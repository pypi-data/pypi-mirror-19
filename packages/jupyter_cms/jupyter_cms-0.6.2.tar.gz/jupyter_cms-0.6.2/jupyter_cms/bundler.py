# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
import os
import shutil
import errno
import nbformat
import fnmatch
import glob
from notebook.utils import url_path_join, url2path
from notebook.base.handlers import IPythonHandler
from notebook.services.config import ConfigManager
from ipython_genutils.importstring import import_item
from tornado import web, gen

class BundlerTools(object):
    '''Set of common tools to aid bundler implementations.'''
    def get_file_references(self, abs_nb_path, version):
        '''
        Gets a list of files referenced either in Markdown fenced code blocks
        or in HTML comments from the notebook. Expands patterns expressed in 
        gitignore syntax (https://git-scm.com/docs/gitignore). Returns the 
        fully expanded list of filenames relative to the notebook dirname.

        NOTE: Temporarily changes the current working directory when called.

        :param abs_nb_path: Absolute path of the notebook on disk
        :param version: Version of the notebook document format to use
        :returns: List of filename strings relative to the notebook path
        '''
        ref_patterns = self.get_reference_patterns(abs_nb_path, version)
        expanded = self.expand_references(os.path.dirname(abs_nb_path), ref_patterns)
        return expanded

    def get_reference_patterns(self, abs_nb_path, version):
        '''
        Gets a list of reference patterns either in Markdown fenced code blocks
        or in HTML comments from the notebook.

        :param abs_nb_path: Absolute path of the notebook on disk
        :param version: Version of the notebook document format to use
        :returns: List of pattern strings from the notebook
        '''
        notebook = nbformat.read(abs_nb_path, version)
        referenced_list = []
        for cell in notebook.cells:
            references = self.get_cell_reference_patterns(cell)
            if references:
                referenced_list = referenced_list + references
        return referenced_list

    def get_cell_reference_patterns(self, cell):
        '''
        Retrieves the list of references from a single notebook cell. Looks for
        fenced code blocks or HTML comments in Markdown cells, e.g.,

        ```
        some.csv
        foo/
        !foo/bar
        ```

        or 

        <!--associate:
        some.csv
        foo/
        !foo/bar
        -->

        :param cell: Notebook cell object
        :returns: List of strings
        '''
        referenced = []
        # invisible after execution: unrendered HTML comment
        if cell.get('cell_type').startswith('markdown') and cell.get('source').startswith('<!--associate:'):
            lines = cell.get('source')[len('<!--associate:'):].splitlines()
            for line in lines:
                if line.startswith('-->'):
                    break
                # Trying to go out of the current directory leads to
                # trouble when deploying
                if line.find('../') < 0 and not line.startswith('#'):
                    referenced.append(line)
        # visible after execution: rendered as a code element within a pre element
        elif cell.get('cell_type').startswith('markdown') and cell.get('source').find('```') >= 0:
            source = cell.get('source')
            offset = source.find('```')
            lines = source[offset + len('```'):].splitlines()
            for line in lines:
                if line.startswith('```'):
                    break
                # Trying to go out of the current directory leads to
                # trouble when deploying
                if line.find('../') < 0 and not line.startswith('#'):
                    referenced.append(line)

        # Clean out blank references
        return [ref for ref in referenced if ref.strip()]

    def expand_references(self, root_path, references):
        '''
        Expands a set of reference patterns by evaluating them against the
        given root directory. Expansions are performed against patterns 
        expressed in the same manner as in gitignore 
        (https://git-scm.com/docs/gitignore).

        :param root_path: Assumed root directory for the patterns
        :param references: List of reference patterns
        :returns: List of filename strings relative to the root path
        '''
        globbed = []
        negations = []
        must_walk = []
        for pattern in references:
            if pattern and pattern.find('/') < 0:
                # simple shell glob
                cwd = os.getcwd()
                os.chdir(root_path)
                if pattern.startswith('!'):
                    negations = negations + glob.glob(pattern[1:])
                else:
                    globbed = globbed + glob.glob(pattern)
                os.chdir(cwd)
            elif pattern:
                must_walk.append(pattern)

        for pattern in must_walk:
            pattern_is_negation = pattern.startswith('!')
            if pattern_is_negation:
                testpattern = pattern[1:]
            else:
                testpattern = pattern
            for root, _, filenames in os.walk(root_path):
                for filename in filenames:
                    joined = os.path.join(root[len(root_path) + 1:], filename)
                    if testpattern.endswith('/'):
                        if joined.startswith(testpattern):
                            if pattern_is_negation:
                                negations.append(joined)
                            else:
                                globbed.append(joined)
                    elif testpattern.find('**') >= 0:
                        # path wildcard
                        ends = testpattern.split('**')
                        if len(ends) == 2:
                            if joined.startswith(ends[0]) and joined.endswith(ends[1]):
                                if pattern_is_negation:
                                    negations.append(joined)
                                else:
                                    globbed.append(joined)
                    else:
                        # segments should be respected
                        if fnmatch.fnmatch(joined, testpattern):
                            if pattern_is_negation:
                                negations.append(joined)
                            else:
                                globbed.append(joined)

        for negated in negations:
            try:
                globbed.remove(negated)
            except ValueError as err:
                pass
        return set(globbed)

    def copy_filelist(self, src, dst, src_relative_filenames):
        '''
        Copies the given list of files, relative to src, into dst, creating
        directories along the way as needed and ignore existence errors.
        Skips any files that do not exist. Does not create empty directories
        from src in dst.

        :param src: Root of the source directory
        :param dst: Root of the destination directory
        :param src_relative_filenames: List of filename relative to src
        '''
        for filename in src_relative_filenames:
            # Only consider the file if it exists in src
            if os.path.isfile(os.path.join(src, filename)):
                parent_relative = os.path.dirname(filename)
                if parent_relative:
                    # Make sure the parent directory exists
                    parent_dst = os.path.join(dst, parent_relative)
                    try:
                        os.makedirs(parent_dst)
                    except OSError as exc:
                        if exc.errno == errno.EEXIST:
                            pass
                        else:
                            raise exc
                shutil.copy2(os.path.join(src, filename), os.path.join(dst, filename))

class BundlerHandler(IPythonHandler):
    def initialize(self, notebook_dir):
        '''
        :param notebook_dir: Root notebook server working directory
        '''
        self.notebook_dir = notebook_dir
        # Create common tools for bundler plugin to use
        self.tools = BundlerTools()

    def get_bundler(self, bundler_id):
        '''
        :param bundler_id: Unique ID within the notebook/jupyter_cms_bundlers
        config section.
        :returns: Dict of bundler metadata with keys label, group, module_name
        :raises KeyError: If the bundler is not registered
        '''
        cm = ConfigManager()
        return cm.get('notebook').get('jupyter_cms_bundlers', {})[bundler_id]

    @web.authenticated
    @gen.coroutine
    def get(self, bundler_id):
        '''
        Executes the requested bundler on the given notebook.

        :param bundler_id: Unique ID of an installed bundler
        :arg notebook: Path to the notebook relative to the notebook directory
            root
        '''
        notebook = self.get_query_argument('notebook')
        abs_nb_path = os.path.join(self.notebook_dir, url2path(notebook))
        try:
            bundler = self.get_bundler(bundler_id)
        except KeyError:
            raise web.HTTPError(404, 'Bundler %s not found' % bundler_id)
        
        module_name = bundler['module_name']
        try:
            # no-op in python3, decode error in python2
            module_name = str(module_name)
        except UnicodeEncodeError:
            # Encode unicode as utf-8 in python2 else import_item fails
            module_name = module_name.encode('utf-8')
        
        try:
            bundler_mod = import_item(module_name)
        except ImportError:
            raise web.HTTPError(500, 'Could not import bundler %s ' % bundler_id)

        # Let the bundler respond in any way it sees fit and assume it will
        # finish the request
        yield gen.maybe_future(bundler_mod.bundle(self, abs_nb_path))

def load_jupyter_server_extension(nb_app):
    web_app = nb_app.web_app
    host_pattern = '.*$'
    bundler_id_regex = r'(?P<bundler_id>[A-Za-z0-9_]+)'
    route_url = url_path_join(web_app.settings['base_url'], '/api/bundlers/%s' % bundler_id_regex)
    web_app.add_handlers(host_pattern, [
        (route_url, BundlerHandler, {'notebook_dir': nb_app.notebook_dir}),
    ])
