from distutils.core import setup, Extension
from distutils.sysconfig import get_python_version
import os, sys, string, platform

# these settings will read setup information from the environment.
# instead of this, the relevant paths can be set directly here:
#
fltk_dir = ""
opengl_dir = ""
# this will be overrridden by environment variables:
fltk_dir = os.environ.get('FLTK_HOME', '')
opengl_dir = os.environ.get('OPENGL_HOME', '')

# add your extensions here
UserDefinedSources = []
# add additional include paths here
UserIncludeDirs = []

# do not edit beyond this point
###########################################################################
# command line configurations
# --disable-gl
# --disable-forms
##########################################################################
doCheckForms = True
doCheckGl = True
isVerbose = True

doMulti = False
doOpenGL = False
doForms = False

# debug flag
doDebug = False
new_args = []
for item in sys.argv:
    if item == '--disable-gl':
        doCheckGl = False
        if isVerbose:
            print("No OpenGL support!")
    elif item == '--disable-forms':
        doCheckForms = False
        if isVerbose:
            print("No Forms support")
    elif item == '--debug':
        doDebug = True
        if isVerbose:
            print("Detected DEBUG build!")
    else:
        new_args.append(item)
sys.argv = new_args

def is_msys_mingw():
    #if os.environ.has_key("MSYSTEM"):
    if "MSYSTEM" in os.environ:
        if os.environ["MSYSTEM"] == "MINGW32":
            return True
    return False

###########################################################################
#
# create proper paths
fltk_lib_dir = os.path.join(fltk_dir, 'lib')
fltk_includes = []
compile_arg_list = []
link_arg_list = []

# whatever is platform dependent
if sys.platform == 'win32' and not is_msys_mingw():
    print("Building for MS Windows, using Visual C++")
    opengl_lib_dir = os.path.join(opengl_dir, 'lib')
    def_list = [('WIN32', '1')]
    compile_arg_list=['/GR']
    lib_dir_list = [fltk_lib_dir, opengl_lib_dir]
    lib_list = ["kernel32", "user32", "gdi32", "winspool", "comdlg32", "Comctl32", "advapi32", "shell32", "ole32", "oleaut32", "uuid", "odbc32", "odbccp32", "wsock32", "fltk", "fltkimages", "fltkforms", "fltkgl", "opengl32", "fltkjpeg", "fltkpng", "fltkz"]
elif sys.platform == 'win32' and is_msys_mingw():
    print("Building for MS Windows, using MinGW")
    if doDebug:
        def_list = [('WIN32', '1'),('_DEBUG', '1')]
    else:
        def_list = [('WIN32', '1')]
    compile_arg_list.append('-Wno-unused-label')
    compile_arg_list.append('-Wno-unused-but-set-variable')
    lib_dir_list = [fltk_lib_dir]
    lib_list = ["fltk", "kernel32", "user32", "gdi32", "winspool", "comdlg32", "Comctl32", "advapi32", "shell32", "oleaut32", "odbc32", "odbccp32", "stdc++", "msvcr71"]
    #link_arg_list=["-Wl,--enable-runtime-pseudo-reloc", "-Wl,--enable-auto-import"]
elif sys.platform.startswith('linux'):
    print("Building for Linux")
    # ugly hack to force distutils to use g++ instead of gcc for linking
    from distutils import sysconfig
    # changes the linker from gcc to g++
    old_init_posix = sysconfig._init_posix
    def my_init_posix():
        if isVerbose:
            print('my_init_posix: changing gcc to g++')
        old_init_posix()
        g = sysconfig._config_vars
        g['LINKCC'] = 'g++ -pthread'
        g['LDSHARED'] = 'g++ -shared'
    sysconfig._init_posix = my_init_posix
    
    def_list = [('UNIX', '1')]
    compile_arg_list.append('-Wno-unused-label')
    compile_arg_list.append('-Wno-unused-but-set-variable')
    compile_arg_list.append('-Wformat=2')
    compile_arg_list.append('-Werror=format-security')
    lib_dir_list = [fltk_lib_dir, '/usr/lib']
    lib_list = ["fltk"]
elif sys.platform in ['freebsd4','freebsd5','freebsd6','freebsd7', 'sunos5']:
    print("Building for: %s"%sys.platform)
    def_list = [('UNIX', '1')]
    lib_dir_list = [fltk_lib_dir,'/usr/X11R6/lib','/usr/lib']
    lib_list = ["fltk"]
elif sys.platform == 'darwin':

    print("Building for  Mac OS X")
    def_list = [('UNIX', '1')]
    lib_dir_list = [fltk_lib_dir]
    lib_list = ["fltk"]
    cpu_type = platform.processor()
    if cpu_type.find("i386"):
        print("i386 CPU variant detected")
        osx_arch = "x86_64"
    elif cpu_type.find("86"):
        print("x86_64 CPU variant detected")
        #osx_arch = "i386"
        osx_arch = "x86_64"
    else:
        print("PowerPC system detected")
        osx_arch = "ppc"

    compile_arg_list=['-arch', osx_arch]
    link_arg_list=['-stdlib=libc++', '-arch', osx_arch, '-framework','ApplicationServices','-framework','Carbon','-framework', 'Cocoa', '-framework','OpenGL','-framework','AGL']

elif sys.platform == 'cygwin':
    print("Building for cygwin using cygwin utilities")
    def_list = [('WIN32', '1'),('NOMINMAX', '1')]
    #lib_dir_list = [fltk_lib_dir,'/usr/lib','/lib','/lib/w32api','/lib/mingw']
    lib_dir_list = [fltk_lib_dir,'/usr/lib','/lib','/lib/w32api','/lib/mingw']
    lib_list = ["fltk", "kernel32", "user32", "gdi32", "winspool", "comdlg32", "Comctl32","advapi32", "shell32", "oleaut32", "odbc32", "odbccp32", "stdc++", "supc++"]
else:
    print("Platform not officially supported!")
    print("You can try to edit the platform specific settings in the file setup.py by creating an entry for the following platform: ", sys.platform)
    sys.exit(0)

    

###########################################################################
# test for fltk configuration (libraries)
def fltk_config(dir):
    global doMulti
    "return library paths and additional libraries that were used to link FLTK"
    needed_libraries = []
    needed_directories = []
    needed_includes = []

    ver_cmd = None
    inc_cmd = None
    lib_cmd = None
    # always use images
    var_string = " --use-images"
    if doCheckGl:
        var_string = var_string + " --use-gl --use-glut"
    if doCheckForms:
        var_string = var_string + " --use-forms"
    try:
        if isVerbose:
            print("Checking fltk-config using FLTK_HOME")
        fltk_dir = os.environ['FLTK_HOME']
        ver_cmd = "sh %s/fltk-config --version"%fltk_dir
        inc_cmd = "sh %s/fltk-config --cxxflags %s"%(fltk_dir, var_string)
        #lib_cmd = "sh %s/fltk-config --use-gl --use-glut --use-images --use-forms --ldflags"%fltk_dir
        lib_cmd = "sh %s/fltk-config --ldflags %s"%(fltk_dir, var_string)
    except:
        if isVerbose:
            print("Checking fltk-config using default installation")
        if is_msys_mingw():
            ver_cmd = "sh fltk-config --version"
            inc_cmd = "sh fltk-config --cxxflags %s"%var_string
            lib_cmd = "sh fltk-config --ldflags %s"%var_string
        else:
            ver_cmd = "fltk-config --version"
            inc_cmd = "fltk-config --cxxflags %s"%var_string
            lib_cmd = "fltk-config --ldflags %s"%var_string

    # version
    result = os.popen(ver_cmd).readlines()
    if len(result) == 0:
        print("No version information for FLTK found!")
    else:
        print("Using FLTK: ", result)
        
    # include flags
    result = os.popen(inc_cmd).readlines()
    if len(result) == 0:
        print("No compile flags found!")
    else:
        inc_list = map(lambda x: x.strip(), result[0].split(' '))
    
        for inc in inc_list:
            if inc[:2] == '-I':
                needed_includes.append(inc[2:])
            if inc.find("_REENTRANT") >= 0:
                doMulti = True
        print("fltk-config includes: ", needed_includes)

    # lib flags
    result = os.popen(lib_cmd).readlines()
    if len(result) == 0:
        print("No link flags found!")
    else:
        lib_list = map(lambda x: x.strip(), result[0].split(' '))
    
        for lib in lib_list:
            if lib[:2] == '-l':
                needed_libraries.append(lib[2:])
            if lib[:2] == '-L':
                needed_directories.append(lib[2:])
        print("fltk-config link paths: ", needed_directories)
        print("fltk-config link libraries: ", needed_libraries)
                
    return (needed_libraries, needed_directories, needed_includes)

###########################################################################
all_include_dirs = ['./src', './contrib','/usr/include']
if fltk_dir != "":
    all_include_dirs.insert(0, fltk_dir)
print(all_include_dirs)
###########################################################################

if not (sys.platform == 'win32' and not is_msys_mingw()):
    
    if is_msys_mingw():
        # a separate method for finding dlls with mingw.

        # fix up the paths for msys compiling.
        import distutils_mod, distutils
        distutils.cygwinccompiler.Mingw32 = distutils_mod.mingcomp

    print("Checking FLTK configuration ... ")
    additional_libs, additional_dirs, additional_includes = fltk_config(fltk_dir)
    
    for item in additional_includes:
        # already included?
        add = True
        for used_inc in all_include_dirs:
            if item == used_inc:
                add = False
                break
        if add:
            all_include_dirs.insert(0, item)

    # check also for multi-threading
    pos = 0
    for item in additional_libs:
        lowercase_item = item.lower()
        if lowercase_item.find("pthread") >= 0:
            doMulti = True
        if (lowercase_item.find("fltk") < 0 and lowercase_item.find("gl") >= 0) or lowercase_item.find("fltk_gl") >= 0:
            doOpenGL = True
        if lowercase_item.find("fltk") >= 0 and lowercase_item.find("forms") >= 0:
            doForms = True
            
    # simply add all the libraries to the front of the used libraries
    lib_list = additional_libs+lib_list
    
    if not doMulti and not is_msys_mingw():
        # disable multi-threading support
        print("FLTK was configured without multi-threading support!")
        compile_arg_list.append("-DDO_NOT_USE_THREADS")
    else:
        print("FLTK was configured with multi-threading support!")

    # On Mac OSX, openGL is always used for FLTK
    if sys.platform == 'darwin':
        doOpenGL = True

    if not doOpenGL:
        # disable OpenGL support
        print("FLTK was configured without OpenGL support!")
        UserDefinedSources.append('./src/Fl_Gl_Stubs.cxx')
        compile_arg_list.append("-DDO_NOT_USE_OPENGL")
    else:
        print("FLTK was configured with OpenGL support!")

    if not doForms:
        # disable Forms support
        print("FLTK was configured without Forms support!")
        UserDefinedSources.append('./src/Fl_Forms_Stubs.cxx')
    else:
        print("FLTK was configured with Forms support!")

    # add all the library paths
    lib_dir_list = additional_dirs+lib_dir_list

    print("done")

###########################################################################



# module declarations
module1 = Extension(name='fltk._fltk',
		    define_macros=def_list,
		    include_dirs = all_include_dirs+UserIncludeDirs,
                    #sources = ['./python/fltk_wrap.cpp',
		    #'./contrib/ListSelect.cpp',
		    #'./contrib/Fl_Table_Row.cxx',
                    #'./contrib/Fl_Table.cxx']+UserDefinedSources,
                    sources = ['./python/fltk_wrap.cpp',
                               './contrib/ListSelect.cpp']+UserDefinedSources,
		    extra_compile_args=compile_arg_list,
                    extra_link_args=link_arg_list,
		    library_dirs=lib_dir_list,
          	    libraries=lib_list)


setup (name = 'pyFltk',
       version = '1.3.4.1',
       author = 'Andreas Held',
       author_email = 'andreasheld@users.sourceforge.net',
       url = 'http://pyfltk.sourceforge.net',
       description = 'This is a Python wrapper for the FLTK',
       ext_modules = [module1],
       packages = ['fltk'],
       package_data={'fltk': ['test/*.*', 'docs/*.*']},
       )



