import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Iterator;
import java.util.PriorityQueue;

public class TreeNavigator{

    public Integer retrievePriority(PriorityQueue<Pair<Node, Integer>> queue, Node a, Integer base)
    {

        if (a.parentCount() == 0)
        {
            // base remains the same
        } else {
            Integer[] parentPriority = new Integer[a.parentCount()];
            Iterator<Node> parentsIterator = a.parentsIterator();
            int index = 0;
            for(Iterator<Node> parent = parentsIterator; parentsIterator.hasNext();)
            {
                parentPriority[index++] = retrievePriority(queue, parent.next(), base+1);
            }
            base = Collections.max(Arrays.asList(parentPriority)) + 1;
        }

        queue.add(new Pair<>(a, base));

        return base;
    }

    public Node[] generateDependency(Node a)
    {
        PriorityQueue<Pair<Node, Integer>> relativeQueue = new PriorityQueue<>();
        retrievePriority(relativeQueue, a, 0);
        Pair<Node, Integer> p;
        HashMap<Node, Integer> leastDuplicate = new HashMap<>();
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
