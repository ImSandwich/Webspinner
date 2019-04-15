
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.PriorityQueue;

class Handler {

    static class Node
    {
        private String name;
        private Node[] dependencies;
        public Node next;
        public Boolean learned;
        public Node(String name, Node[] dependencies)
        {
            this.name = name;
            this.dependencies = dependencies;
            learned = false;
        }

        public Node[] getDependencies()
        {
            return dependencies;
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

        public void setDependencies(Node[] l)
        {
            dependencies = l;
        }

        @Override
        public String toString()
        {
            return name;
        }
    }

    class Pair<A, B extends Comparable<B>> implements Comparable<Pair<A, B>>
    {
        public  A e1;
        public  B e2;
        public Pair (A element1, B element2)
        {
            e1 = element1;
            e2 = element2;
        }


        @Override
        public int compareTo(Pair<A, B> o) {

            return e2.compareTo(o.e2);
        }


        @Override
        public String toString()
        {
            return e1.toString() + "," + e2.toString();
        }
    }

    public Integer retrievePriority(PriorityQueue<Pair<Node, Integer>> queue, Node a, Integer base)
    {
        if (a.isEndNode())
        {
            // base remains the same
        } else {
            Integer[] childrenPriority = new Integer[a.dependencies.length];
            for (int i = 0; i < a.dependencies.length; i++)
            {
                childrenPriority[i] = retrievePriority(queue, a.dependencies[i], base + 1);
            }
            base = Collections.max(Arrays.asList(childrenPriority)) + 1;
        }

        queue.add(new Pair<>(a, base));

        return base;
    }

    public Node[] priority(Node a)
    {
        PriorityQueue<Pair<Node, Integer>> relativeQueue = new PriorityQueue<>();
        retrievePriority(relativeQueue, a, 0);
        Handler.Pair<Handler.Node, Integer> p;
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
