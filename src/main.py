from textnode import TextNode, TextType

def main():
    node = TextNode("My test node", TextType.PLAIN, "https://myurl:1234")
    print(node)
    
if __name__ == "__main__":
    main()