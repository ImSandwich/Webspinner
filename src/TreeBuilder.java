/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import java.util.HashMap;
import java.util.LinkedList;

public class TreeBuilder {
    private TreeNavigator treeNavigator;

    public static void printNode(Node node, int index)
    {
        for (int i = 0; i < index; i++ ) System.out.print(" ");
        System.out.print(node);
        System.out.println();
    }

    public TreeBuilder(String startNode, int expanse)
    {
        treeNavigator = new TreeNavigator();
        HashMap<String, Node> discovered = new HashMap<>();
        LinkedList<Pair<Node, String>> queryQueue = new LinkedList<>();
        LinkedList<Pair<Node, String>> followingQueryQueue = new LinkedList<>();
        queryQueue.push(new Pair<>(null, startNode));
        while (expanse > 0)
        {
            Pair<Node,String> nextNode;
            while (queryQueue.size()>0) // nextNode : (Parent node, article names linked to the parent node)
            {
                nextNode = queryQueue.pop();
                Node currentNode;
                if (discovered.containsKey(nextNode.e2)) // check if we have expanded the article already
                {
                    currentNode = discovered.get(nextNode.e2);
                } else {
                    currentNode = new Node(nextNode.e2);
                    System.out.println("Added: " + nextNode.e2);
                    discovered.put(nextNode.e2, currentNode); // add article to list of expanded articles
                    WebScraper.WikipediaResponse response = WebScraper.scrapWikipedia(nextNode.e2);
                    for(String urls : response.linkedPages.values())
                    {
                        followingQueryQueue.add(new Pair<>(currentNode, urls));  // new Pair : (Current node, article names linked to the current node)
                    }
                }
                currentNode.addParent(nextNode.e1);


            }
            queryQueue.clear();
            for (int i = 0; i < followingQueryQueue.size();i++) queryQueue.add(followingQueryQueue.get(i));
            followingQueryQueue.clear();
            expanse--;
        }
        Node node = discovered.get(startNode);
        printNode(node, 0);

    }
}
