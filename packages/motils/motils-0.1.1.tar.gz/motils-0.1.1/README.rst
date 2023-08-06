The motils package includes the following functions:
 - file_to_string(file_name): converts a file to string and returns the string
 - remove_commas(file_name, new_file_name=None): removes commas from a file and replaces them with newlines
 - zip_files(file_list, output_path): zips a list of files and returns the path to the zip file
 - debug(debug_string, to_debug): prints timestamp + string only if the to_debug flag is True
 - create_folder_if_needed(path): creates a folder if it doesn't already exist
 - file_len(file_name): returns the length of the file in lines
 - targz_folder(folder, archive_name=None): returns a path to tar.gz folder made out of folder
 - write_bash_script(command_line, write_folder, script_name="run_script.sh"):  writes a bash script and returns its path
 - merge_two_dicts(x, y): returns a merged dictionary
 - is_number(s): returns True if the string is a number

I have used several of these functions in my work on a daily basis, so why not publish them?

Written by Moran Neuhof, 2017