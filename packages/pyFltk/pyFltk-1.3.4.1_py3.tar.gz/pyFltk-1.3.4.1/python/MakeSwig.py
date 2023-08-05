import os, os.path, sys, string, shutil, glob, pickle

# this file defines the commands for updating the init
# methods (constructors) of the widget classes for pyFLTK
# run this before issuing the SWIG command


PythonOwns = ['Fl_Preferences']


def is_msys_mingw():
    #if os.environ.has_key("MSYSTEM"):
    if "MSYSTEM" in os.environ:
        if os.environ["MSYSTEM"] == "MINGW32":
            return True
    return False


if __name__=='__main__':
    
    # call SWIG
    include = ['-I/usr/include']
    try:
        fltk_dir = os.environ['FLTK_HOME']
        include.insert(0, "-I%s"%fltk_dir)
    except:
        print("Using default location for FLTK!")
        if is_msys_mingw():
            result = os.popen('sh fltk-config --cxxflags').readlines()
        else:
            result = os.popen('fltk-config --cxxflags').readlines()
        #print(result)
        if len(result) > 0:
            p_inc = map(lambda x: x.strip(), result[0].split(' '))
            for item in p_inc:
                #if string.find(item, '-I') == 0:
                if item.find('-I') == 0:
                    include.insert(0, item)
        else:
            print("FLTK not found!")
            sys.exit(0)
    
    #add_incl = string.join(include, ' ')
    add_incl = ' '.join(include)

    # command line for swig-1.3.28 or later
    versionIdentifier = ""
    if sys.version >= "3.0":
        versionIdentifier = "-DPYTHON3"
    cmd_line = "swig -w312 -w451 -w473 -I../swig %s -DFL_EXPORT -DPYTHON %s -module fltk -c++ -python -shadow -modern -fastdispatch -o fltk_wrap.cpp ../swig/fltk.i "%(add_incl, versionIdentifier)
    # command line for swig-1.3.27
    # cmd_line = "swig -w312 -w451 -w473 -I../swig %s -DFL_EXPORT -DPYTHON -module fltk -c++ -python -shadow -modern -dirprot -o fltk_wrap.cpp ../swig/fltk.i "%add_incl
    if is_msys_mingw():
        # adjust the paths so that MinGW can understand it
        cmd_line = cmd_line.replace("\\", "/")
        cmd_line = cmd_line.replace("c:", "/c")
        cmd_line = cmd_line.replace("C:", "/c")

        import tempfile
        tmpfn = tempfile.mktemp(suffix='run_swig')
        tmpf = open(tmpfn, "w+b")
        tmpf.write(cmd_line)
        tmpf.close()
        r = os.system("sh %s" % tmpfn)

        os.remove(tmpfn)
        if r != 0:
            raise DistutilsExecError("command '%s' failed with exit status :%d: command was :%s:.  " % (cmd[0], r, cmpl))
        
        print("return value of the command is :%s:" % r)
    else:
        print(cmd_line)
        os.system(cmd_line)

    #print("Copy fltk.py")
    if os.path.isdir("../fltk"):
        shutil.rmtree("../fltk");
    os.mkdir("../fltk");
    os.mkdir("../fltk/test");
    os.mkdir("../fltk/docs");
    
    shutil.copyfile("fltk.py", "../fltk/__init__.py")
    #print(glob.glob("../test/*.py"))
    for x in glob.glob("../test/*.py"): shutil.copy(x, "../fltk/test")
    for x in glob.glob("../test/*.html"): shutil.copy(x, "../fltk/test")
    for x in glob.glob("../test/*.gif"): shutil.copy(x, "../fltk/test")
    for x in glob.glob("../docs/*.html"): shutil.copy(x, "../fltk/docs")
    for x in glob.glob("../docs/*.jpg"): shutil.copy(x, "../fltk/docs")
             


    
    
