/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import java.util.HashMap;
import java.util.LinkedList;

public class MapBuilder {
    private Handler handler;

    public static void printNode(Handler.Node node, int index)
    {
        for (int i = 0; i < index; i++ ) System.out.print(" ");
        System.out.print(node);
        System.out.println();
        for (int i = 0; i < node.children.size(); i++)
        {
            printNode(node.children.get(i), index+1);
        }
    }
    public MapBuilder(String startNode, int expanse)
    {
        handler = new Handler();
        HashMap<String, Handler.Node> discovered = new HashMap<>();
        LinkedList<Pair<Handler.Node, String>> queryQueue = new LinkedList<>();
        LinkedList<Pair<Handler.Node, String>> followingQueryQueue = new LinkedList<>();
        queryQueue.push(new Pair<>(null, startNode));
        while (expanse > 0)
        {
            Pair<Handler.Node,String> nextNode;
            while (queryQueue.size()>0) // nextNode : (Parent node, article names linked to the parent node)
            {
                nextNode = queryQueue.pop();
                Handler.Node currentNode;
                if (discovered.containsKey(nextNode.e2)) // check if we have expanded the article already
                {
                    currentNode = discovered.get(nextNode.e2);
                } else {
                    currentNode = new Handler.Node(nextNode.e2);
                    System.out.println("Added: " + nextNode.e2);
                    discovered.put(nextNode.e2, currentNode); // add article to list of expanded articles
                    WebScraper.WikipediaResponse response = WebScraper.scrapWikipedia(nextNode.e2);
                    for(String urls : response.linkedPages.values())
                    {
                        followingQueryQueue.add(new Pair<>(currentNode, urls));  // new Pair : (Current node, article names linked to the current node)
                    }
                }
                currentNode.addDependency(nextNode.e1);
                if (nextNode.e1 != null) nextNode.e1.children.add(currentNode);

            }
            queryQueue.clear();
            for (int i = 0; i < followingQueryQueue.size();i++) queryQueue.add(followingQueryQueue.get(i));
            followingQueryQueue.clear();
            expanse--;
        }
        Handler.Node node = discovered.get(startNode);
        printNode(node, 0);

    }
}
