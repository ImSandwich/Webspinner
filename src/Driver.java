import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */
public class Driver {

    public static Node generateTestMap(Integer nodesCount, Integer edgesCount)
    {
        Node[] nodes = new Node[nodesCount];
        Random randomizer = new Random();
        for (int i = 0; i < nodesCount; i++) nodes[i] = new Node("Node"+i);
        HashMap<Pair<String, String>, Boolean> connections = new HashMap<>();
        ArrayList<Node> added = new ArrayList<>();
        added.add(nodes[0]);
        for (int i = 0; i < edgesCount; i++)
        {
            Node startingNode = added.get(randomizer.nextInt(added.size()));
            Node endingNode = null;
            while (endingNode == null || endingNode == startingNode || connections.containsKey(new Pair<>(startingNode.toString(), endingNode.toString())))
            {
                endingNode = nodes[randomizer.nextInt(nodes.length)];
            }
            connections.put(new Pair<>(startingNode.toString(), endingNode.toString()), true);
            if (!added.contains(endingNode)) added.add(endingNode);
            startingNode.addChild(endingNode);
        }
        return nodes[0];
    }

    public static void main(String[] args) {


        /*
        Node A = new Node("a");
        Node B = new Node("b");
        Node C = new Node("c");
        Node D = new Node("d");
        Node E = new Node("e");
        Node F = new Node("f");
        Node G = new Node("g");
        E.addChild(F);
        D.addChild(G);
        C.addChild(D);
        A.addChild(new Node[]{B, C, D});
        B.addChild(new Node[]{E,C});
        //G.addChild(A);

         */


        Node A = generateTestMap(8,50);
         
        
        TreeBuilder treeBuilder = new TreeBuilder(A);


        treeBuilder.printTree();
        Node testNode = treeBuilder.randomNode();

        Node[] dependencyTree = treeBuilder.treeNavigator.generateDependency(testNode);
        System.out.println("Reading list for " + testNode.toString());
        for(Node n : dependencyTree)
        {
            System.out.println(n);
        }







    }
}
