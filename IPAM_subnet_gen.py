

def main():
    #start with 0
    #increment by 4 each loop
    #add to string "10.0.4."
    host=3
    network=64
    for i in range(network):
        print(f'10.0.4.{host}')
        host+=4
        i+=1
        
    print("END")
        
if __name__ == '__main__':
    main()