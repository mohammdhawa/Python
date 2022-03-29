
the_file = None
the_tries = 5

while the_tries>0:
    
    try: # to open the file
        print("Enter the file name with absolute path to open")
        
        print(f"You have {the_tries} tries left")
        
        print("Example: D:\Python\Files\yourfile.extension")
        
        file_name_and_path = input("Enter flie name: ").strip()
        
        the_file = open(file_name_and_path, 'r')
        
        print(the_file.read())
        
        break
    
    except FileNotFoundError:
        
        print("File not found please be sure the name is valid")
        
        print(f"{the_tries} Tries left")
    
        the_tries -=1
    except:
        
        print("Error happened")
        
    finally:
        
        if the_file is not None:
            
            the_file.close()
            
            print("File closed.")
else:
        
    print("All tries is done")
        
