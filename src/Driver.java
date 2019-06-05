import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Random;
import java.util.regex.Pattern;
import java.io.*;
/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */
public class Driver {

    public static void readDBPedia(String file, int limit) throws IOException {
        BufferedReader br =  new BufferedReader(new FileReader(file));
        String line ;
        Pattern tagRecognizer = Pattern.compile("<(.*?)>");
        int count = 0;
        while ((line = br.readLine()) != null)
        {
            count++;
            /*
            limit--;
            Matcher tagMatcher = tagRecognizer.matcher(line);
            String parent = null, child = null;
            int index=0;
            while(tagMatcher.find())
            {
                String matched = tagMatcher.group();
                String[] decompose = matched.substring(1,matched.length()-1).split("/");
                if (index == 0) parent = decompose[decompose.length-1];
                else if (index == 2) child = decompose[decompose.length-1];
                index++;


            }

            if (index != 3 || parent == null || child == null) continue;
            System.out.println(parent + "->" + child);


            if (limit==0) break;

             */
        }
        System.out.println(count);
        br.close();
    }

    public static void serializeToFile(Object obj, String file) throws IOException
    {
        FileOutputStream fileOutputStream = new FileOutputStream(file);
        ObjectOutputStream objectOutputStream = new ObjectOutputStream(fileOutputStream);
        objectOutputStream.writeObject(obj);
        objectOutputStream.close();
        fileOutputStream.close();
    }

    public static Object deserializeFromFile(String file) throws IOException, ClassNotFoundException
    {
        FileInputStream fileInputStream = new FileInputStream(file);
        ObjectInputStream objectInputStream = new ObjectInputStream(fileInputStream);
        Object obj = objectInputStream.readObject();
        fileInputStream.close();
        objectInputStream.close();
        return obj;
    }

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

    public static void main(String[] args) throws IOException, ClassNotFoundException {



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


        //readDBPedia("C:\\Users\\Kuan\\Downloads\\page_links_en.nt\\page_links_en.nt",100);

        HashMap<String, Node> hashMap = new HashMap<>();
        hashMap.put("One",A);
        hashMap.put("Three", B);
        serializeToFile(hashMap,"hash.ser");
        HashMap<String, Node> readMap = (HashMap<String,Node>)deserializeFromFile("hash.ser");
        System.out.println(readMap.get("Three"));
        /*
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



         */





    }
}
