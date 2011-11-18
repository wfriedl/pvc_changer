
import os, shutil
import pvc_changer as update

## path is relative to where nose is run from?!
src_file = r"tests/EZChrom Install Package.vdproj"
test_file = r"tests/test.vdproj"


def test_regex_code():
    test_code = """            "ProductCode" = "8:{35424778-8534-431B-9492-5CD84B1EDE03}"\r\n"""
    m = update.productcode_re.search(test_code)
    assert m is not None, "should have found this: %s"%test_code.strip()
    assert m.group(1) == "35424778-8534-431B-9492-5CD84B1EDE03", "found wrong code: %s"%m.group(1)

def test_regex_version():
    test_ver = """            "ProductVersion" = "8:1.0.8000099"\r\n"""
    m = update.productversion_re.search(test_ver)
    assert m is not None, "should have found this: %s"%test_ver.strip()
    assert m.group(1) == "1.0.8000099", "found wrong version: %s"%m.group(1)

class TestProductVersioner():
    """ 
        Test the general 'updating' of vs2010 setup packages 
        ** requires a source .vdproj file for testing
    """

    def setup(self):
        assert os.path.exists(src_file), "need to set source vdproj path... currently: %s"%src_file
        shutil.copyfile(src_file, test_file)
        assert os.path.exists(test_file), "missing test file: %s"%test_file

    def teardown(self):
        os.remove(test_file)
        assert not os.path.exists(test_file), "missing test file: %s"%test_file

    def test_replace(self):
        update.replace_code_and_version(test_file)

        self.compare_files()

    def test_parse(self):
        args = update.parse_commands(['-f', test_file])
        assert len(args.code) == 36, "wrong code length: %s"%len(args.code)
        code1 = args.code
        assert args.version == '1.0.0', "wrong version: %s"%args.version
        args = update.parse_commands(['-v', '1.0.127', '-f', test_file])
        assert args.version == '1.0.127', "wrong version: %s"%args.version
        assert len(args.code) == 36, "wrong code length: %s"%len(args.code)
        assert code1 != args.code, "these shouldn't match: %s != %s"%(code1, args.code)
        assert 'test.vdproj' in args.vdproj, "Should be our test file: %s"%args.vdproj

    def test_everything(self):
        build = 125
        args = update.parse_commands(['-v','1.0.%d'%build, '-f', test_file])
        update.replace_code_and_version(args.vdproj, args.version, args.code)

        self.compare_files()

    def compare_files(self):
        fsrc = open(src_file)
        ftst = open(test_file)
        for s,t in zip(iter(fsrc), iter(ftst)):
            if update.productcode_re.search(s) or update.productversion_re.search(s):
                assert s != t, "These shouldn't match: %s != %s"%(s.strip(),t.strip())
            else:
                assert s == t, "These should match: %s == %s"%(s.strip(), t.strip())
        fsrc.close()
        ftst.close()


