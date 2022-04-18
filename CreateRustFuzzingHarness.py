#!/usr/bin/python 3

'''
Simple script to create rust fuzzing harness
Author: @TanoyBose
License: Attribution 4.0 International (CC BY 4.0)
License Information: https://creativecommons.org/licenses/by/4.0/legalcode
'''

class libfuzzerHarness:
    def  __init__(self, harness_name = 'test.rs', no_main = 'y', use_crate = '2', module_name = '', function_call = ['']):
        self.harness_name = harness_name
        self.no_main = no_main
        self.use_crate = use_crate
        self.module_name = module_name
        self.function_call = function_call
    def create_harness(self):
        '''#![no_main]
        use libfuzzer_sys::fuzz_target;
        use adblock::lists::{parse_filter, FilterFormat};
        fuzz_target!(|data: &[u8]| {
            if let Ok(filter) = std::str::from_utf8(data) {
                parse_filter(filter, true, FilterFormat::Standard);
            }
        });
        '''
        harness_data = ''
        if self.no_main == 'y':
            harness_data = harness_data + '#![no_main]\n'
        else:
            print("Currently libfuzzer harness is implemented without main. Please retry.")
            exit()
        if self.use_crate == '1':
            harness_data = harness_data + '#[macro_use]\n'
            harness_data = harness_data + 'extern crate libfuzzer_sys;\n' + self.module_name + '\n'
        else:
            harness_data = harness_data + 'use libfuzzer_sys::fuzz_target;\n' + self.module_name + '\n'
        harness_data = harness_data + 'fuzz_target!(|data: &[u8]| {\n\tif let Ok(fuzzer_input) = std::str::from_utf8(data) {\n'
        for eachData in range(0,len(self.function_call)):
            harness_data = harness_data + '\t\t' + self.function_call[eachData] + '\n'
        harness_data = harness_data + '\t}\n});\n'
        harness_file = open(self.harness_name,"w")
        harness_file.write(harness_data)
        harness_file.close()
    def libfuzzer_fuzzing_steps():
        '''
        future method to implement automation of the fuzzing
        '''
        pass

class aflHarness:
    def  __init__(self, harness_name = 'test.rs', no_main = 'n', use_crate = '1', module_name = '', function_call = ['']):
        self.harness_name = harness_name
        self.no_main = no_main
        self.use_crate = use_crate
        self.module_name = module_name
        self.function_call = function_call
    def create_harness(self):
        '''
        #[macro_use]
        extern crate afl;
        use adblock::lists::{parse_filter, FilterFormat};
        fn main() {
            fuzz!(|data: &[u8]| {
                if let Ok(filter) = std::str::from_utf8(data) {
                    parse_filter(filter, true, FilterFormat::Standard);
                }
            });
        }
        '''
        if self.no_main == 'y':
            print("[-] Current setup allows AFL harness to be implemented with Main function. Please retry.")
            exit()
        harness_data = ''
        if self.use_crate == '1':
            harness_data='#[macro_use]\nextern crate afl;\n' + self.module_name + '\n'
        else:
            print("[-] Current implementation requires to use afl as an extern crate. Please retry.")
            # For future implementation implement use afl::fuzz
            exit()
        harness_data = harness_data + 'fn main() {\n\tfuzz!(|data: &[u8]| {\n\t\tif let Ok(fuzzer_input) = std::str::from_utf8(data) {\n'
        for eachData in range(0,len(self.function_call)):
            harness_data = harness_data + '\t\t' + self.function_call[eachData] + '\n'
        harness_data = harness_data +'\t\t}\n\t});\n}'
        harness_file = open(self.harness_name, "w")
        harness_file.write(harness_data)
        harness_file.close()
    def afl_fuzzing_steps():
        '''
        future method to implement automation of the fuzzing
        '''
        pass

def main():
    harness_name = input("Name for the harness (default: test.rs): ")
    if harness_name == '':
        harness_name = 'test.rs'
    harness_type = input("Enter 1 for libfuzzer, or 2 for afl (default 1): ")
    if harness_type == '2':
        pass
    else:
        harness_type = '1'
    #print("[!] Remember, when you need to run afl-fuzzer, you might need to rename the file to main.rs and place it in the src directory")
    use_crate = input("Enter 1 to use crates, or 2 to fuzz function directly: (default 2): ")
    if use_crate == '1':
        pass
    else:
        use_crate = 2
    no_main = input("Define no_main ([y]/n): ")
    if no_main == 'n':
        pass
    else:
        no_main = 'y'
    if (use_crate == '1'):
        module_name = input("Please input the module you want to use (e.g. - extern crate url;): ")
        number_of_function_calls = 1
        try:
            number_of_function_calls = int(input("Please input the number of function calls you want to perform (default 1): "))
        except:
            number_of_function_calls = 1
        print("[!] Remember, the input variable to the function call you want to fuzz should always be fuzzer_input")
        function_call=[]
        for eachFunctionCalled in range(0,number_of_function_calls):
            function_call.append(input("Please input the function call you want to fuzz (e.g. - let _ = url::Url::parse(&fuzzer_input);): "))
    else:
        module_name = input("Please input the module you want to use (e.g. - use adblock::request::Request;): ")
        number_of_function_calls = 1
        try:
            number_of_function_calls = int(input("Please input the number of function calls you want to perform (default 1): "))
        except:
            number_of_function_calls = 1
        print("[!] Remember, the input variable to the function call you want to fuzz should always be fuzzer_input")
        function_call=[]
        for eachFunctionCalled in range(0,number_of_function_calls):
            function_def = input("Please input the function you want to fuzz (e.g. - Request::from_url(&format!(\"https://{}\", fuzzer_input));): ")
            function_call.append(function_def)
    if (harness_type == '2'):
        fuzzerHarness = aflHarness(harness_name, no_main, use_crate, module_name, function_call)
        fuzzerHarness.create_harness()
    else:
        fuzzerHarness = libfuzzerHarness(harness_name, no_main, use_crate, module_name, function_call)
        fuzzerHarness.create_harness()

if __name__ == '__main__':
    main()
