/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.PriorityQueue;
import java.util.Random;
public class TreeBuilder {
    public TreeNavigator treeNavigator;
    private Node root;
    private HashMap<String, Node> hashTree;
    public static void printNode(Node node, int index)
    {
        for (int i = 0; i < index; i++ ) System.out.print(" ");
        System.out.print(node);
        System.out.println();
    }

    public void printTree()
    {
        ArrayList<Node> existingNodes = new ArrayList<>(Arrays.asList(hashTree.values().toArray(new Node[hashTree.values().size()])));
        for (int i = 0; i < existingNodes.size(); i++)
        {
            System.out.print(existingNodes.get(i).toString() + " <- ");
            for (Iterator<Node> iterator = existingNodes.get(i).parentsIterator(); iterator.hasNext();)
            {
                System.out.print(iterator.next().toString() + " ");
            }
            System.out.println();
        }
    }

/* Obsolete - For testing purposes only
    public TreeBuilder(String startNode, int expanse)
    {
        treeNavigator = new TreeNavigator();
        hashTree = new HashMap<>();

        LinkedList<Pair<Node, String>> queryQueue = new LinkedList<>();
        LinkedList<Pair<Node, String>> followingQueryQueue = new LinkedList<>();
        queryQueue.push(new Pair<>(null, startNode));
        while (expanse > 0)
        {
            Pair<Node,String> nextNode;
            while (queryQueue.size() > 0) // nextNode : (Parent node, article names linked to the parent node)
            {
                nextNode = queryQueue.pop();
                Node currentNode;
                if (hashTree.containsKey(nextNode.e2)) // check if we have expanded the article already
                {
                    currentNode = hashTree.get(nextNode.e2);
                } else {
                    currentNode = new Node(nextNode.e2);
                    System.out.println("Added: " + nextNode.e2);
                    hashTree.put(nextNode.e2, currentNode); // add article to list of expanded articles
                    WebScraper.WikipediaResponse response = WebScraper.scrapWikipedia(nextNode.e2);
                    for(String urls : response.linkedPages.values())
                    {
                        followingQueryQueue.add(new Pair<>(currentNode, urls));  // new Pair : (Current node, article names linked to the current node)
                    }
                }

                if (nextNode.e1 != null) // exclude the head node from having a parent
                {
                    currentNode.addParent(nextNode.e1);
                    nextNode.e1.addChild(currentNode);
                }

            }
            queryQueue.clear();
            for (int i = 0; i < followingQueryQueue.size();i++) queryQueue.add(followingQueryQueue.get(i));
            followingQueryQueue.clear();
            expanse--;
        }



    }

 */
    public Integer getNumberCycles(Node root)
    {
        HashMap<Node, Boolean> visited =  new HashMap<>();
        visited.put(root, true);
        return DFSTraversalCollisions(root,visited);
    }

    private Integer DFSTraversalCollisions(Node current, HashMap<Node, Boolean> visited)
    {
        if (current == null) return 0;
        Integer total = 0;
        for (Iterator<Node> childrenIterator = current.childrenIterator(); childrenIterator.hasNext();)
        {
            Node child = childrenIterator.next();
            if (visited.containsKey(child) && visited.get(child))
            {
                total++;
            } else {
                visited.put(child, true);
                total += DFSTraversalCollisions(child, visited);
                visited.put(child, false);
            }
        }
        return total;
    }

    public TreeBuilder(Node root)
    {
        hashTree = new HashMap<>();
        treeNavigator = new TreeNavigator();
        this.root = root;
        unfold(this.root, hashTree);
        prune(this.root);
    }

    private void unfold (Node node, HashMap<String, Node> map)
    {
        map.put(node.toString(), node);
        for (Iterator<Node> childrenIterator = node.childrenIterator(); childrenIterator.hasNext();)
        {
            Node child = childrenIterator.next();
            if (!map.containsKey(child.toString()))
            unfold(child, map);
        }
    }
    private boolean prune(Node root)
    {
        /* Pruning, N^2 operation
        Assumption:
        1. The entire tree is connected (unidirectionally, from parent to child)

         */

        int TEST_NEG = 0;

        PriorityQueue<Pair<Node[], Double>> edges = new PriorityQueue<>();

        HashMap<Node, Integer> unionFindLookup = new HashMap<>();
        UnionFind unionFind = new UnionFind(hashTree.values().size());

        int lookupIndex = 0;
        for (Iterator<Node> nodeIterator = hashTree.values().iterator(); nodeIterator.hasNext();)
        {
            unionFindLookup.put(nodeIterator.next(), lookupIndex++);
        }


        for (Iterator<Node> nodeIterator = hashTree.values().iterator(); nodeIterator.hasNext();)
        {
            Node n = nodeIterator.next();
            for (Iterator<Node> nodeChildrenIterator = n.childrenIterator(); nodeChildrenIterator.hasNext();)
            {
                Node c = nodeChildrenIterator.next();
                edges.add(new Pair<>(new Node[]{n, c}, c.complexity()-n.complexity()));
                unionFind.union(unionFindLookup.get(n), unionFindLookup.get(c));
            }
        }

        assert(unionFind.allConnected()); // Make sure that assumption is fulfilled
        ArrayList<Node[]> arrayEdges = new ArrayList<>();
        Pair<Node[], Double> p = null;
        while ((p = edges.poll()) != null)
        {
            System.out.println(p.e1[0] + "->" + p.e1[1] + ": " + p.e2);
            arrayEdges.add(p.e1);
            if (p.e2 < 0) TEST_NEG++;
        }

        ArrayList<Node[]> removedEdges = new ArrayList<>();

        boolean optimalSolutionFound = false;
        int cycleCount = getNumberCycles(root);
        for (int attempt = 0; attempt < arrayEdges.size(); attempt++)
        {
            unionFind.clear();
            Node[] attemptRemoved = arrayEdges.get(attempt);
            attemptRemoved[0].removeChild(attemptRemoved[1]);
            attemptRemoved[1].removeParent(attemptRemoved[0]);

            for (Iterator<Node> nodeIterator = hashTree.values().iterator(); nodeIterator.hasNext();)
            {
                Node n = nodeIterator.next();
                for (Iterator<Node> nodeChildrenIterator = n.childrenIterator(); nodeChildrenIterator.hasNext();)
                {
                    Node c = nodeChildrenIterator.next();
                    unionFind.union(unionFindLookup.get(n), unionFindLookup.get(c));
                }
            }
            int newCycleCount = getNumberCycles(root);
            if (!unionFind.allConnected() || newCycleCount >= cycleCount)
            {
                attemptRemoved[0].addChild(attemptRemoved[1]);
                attemptRemoved[1].addParent(attemptRemoved[0]);
            }
            else
            {
                removedEdges.add(attemptRemoved);
                System.out.println("Removed " + attemptRemoved[0] + "->" + attemptRemoved[1]);
                cycleCount = newCycleCount;
                if (cycleCount == 0)
                {
                    optimalSolutionFound = true;
                    break;
                }
            }
        }

        if (optimalSolutionFound)
        {
            System.out.println("Tree pruned and cycle removed");
            System.out.println("Negatives: " + TEST_NEG + " Removed: " + removedEdges.size());
            return true;
        } else {
            System.out.println("Error removing tree");
            for (Iterator<Node[]> iterator = removedEdges.iterator(); iterator.hasNext();)
            {
                Node[] attemptRemoved = iterator.next();
                attemptRemoved[0].addChild(attemptRemoved[1]);
                attemptRemoved[1].addParent(attemptRemoved[0]);
            }
            return false;
        }
    }

    public Node randomNode()
    {
        Random randomizer = new Random();
        return  hashTree.values().toArray(new Node[hashTree.values().size()])[randomizer.nextInt(hashTree.values().size())];
    }
}
