
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.PriorityQueue;

class Handler {

    static class Node
    {
        private String name;
        public ArrayList<Node> dependencies;
        public ArrayList<Node> children;
        public Node next;
        public Boolean learned;
        public Node(String name)
        {
            this.name = name;
            this.dependencies = new ArrayList<>();
            this.children = new ArrayList<>();
            learned = false;
        }

        public void addDependency(Node e)
        {
            if (e == null) return;
            if (!dependencies.contains(e)) dependencies.add(e);
        }

        public void removeDependency(Node e)
        {
            if (dependencies.contains(e)) dependencies.remove(e);
        }

        public  Boolean isEndNode()
        {
            if (dependencies == null) return true;
            for (Node d: dependencies)
            {
                if (!d.learned) return false;
            }
            return true;
        }


        @Override
        public String toString()
        {
            return name;
        }
    }

    class NodeIntegerPair implements Comparable<NodeIntegerPair>
    {
        public  Node e1;
        public  Integer e2;
        public NodeIntegerPair(Node element1, Integer element2)
        {
            e1 = element1;
            e2 = element2;
        }


        public int compareTo(NodeIntegerPair o) {

            return e2.compareTo(o.e2);
        }


        @Override
        public String toString()
        {
            return e1.toString() + "," + e2.toString();
        }
    }

    public Integer retrievePriority(PriorityQueue<NodeIntegerPair> queue, Node a, Integer base)
    {

        if (a.isEndNode())
        {
            // base remains the same
        } else {
            Integer[] childrenPriority = new Integer[a.dependencies.size()];
            for (int i = 0; i < a.dependencies.size(); i++)
            {
                childrenPriority[i] = retrievePriority(queue, a.dependencies.get(i), base + 1);
            }
            base = Collections.max(Arrays.asList(childrenPriority)) + 1;
        }

        queue.add(new NodeIntegerPair(a, base));

        return base;
    }

    public Node[] generateDependency(Node a)
    {
        PriorityQueue<NodeIntegerPair> relativeQueue = new PriorityQueue<>();
        retrievePriority(relativeQueue, a, 0);
        NodeIntegerPair p;
        HashMap<Handler.Node, Integer> leastDuplicate = new HashMap<>();
        ArrayList<Node> adder = new ArrayList<>();
        while ((p = relativeQueue.poll()) != null)
        {
            if (!leastDuplicate.containsKey(p.e1))
            {
                leastDuplicate.put(p.e1, p.e2);
                adder.add(p.e1);
            }
        }
        return  adder.toArray(new Node[adder.size()]);
    }


}
