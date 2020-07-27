def median(iterable):
    items = sorted(iterable)
    if len(items) == 0:
        raise ValueError("median() arg is an empty serier")
    
    median_index = (len(items) - 1) // 2
    if len(items) % 2 != 0:
        return items[median_index]
    return (items[median_index] + items[median_index + 1]) / 2


def main():
    try:
        median([])
    except ValueError as e:
        print("Payload repr:", repr(e))
        print("Payload str:", str(e))
        
        
if __name__ == "__main__":
    main()