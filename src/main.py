from textnode import TextNode, TextType
from utils.convert import split_nodes_image

def main():
    node = TextNode("My test node", TextType.TEXT, "https://myurl:1234")
    print(node)


    ## TEST CODE TODO: REMOVE
    node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
    new_nodes = split_nodes_image([node])
    print(new_nodes)
    
if __name__ == "__main__":
    main()