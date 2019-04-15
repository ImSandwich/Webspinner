/* *****************************************************************************
 *  Name:
 *  Date:
 *  Description:
 **************************************************************************** */
public class Driver {

    public static void main(String[] args) {
        Handler handler = new Handler();
        Handler.Node A = new Handler.Node("a", null);
        Handler.Node B = new Handler.Node("b", null);
        Handler.Node C = new Handler.Node("c", null);
        Handler.Node D = new Handler.Node("d", null);
        Handler.Node E = new Handler.Node("e", null);
        Handler.Node F = new Handler.Node("f", null);
        Handler.Node G = new Handler.Node("g", null);
        E.setDependencies(new Handler.Node[]{F});
        D.setDependencies(new Handler.Node[]{G});
        C.setDependencies(new Handler.Node[]{D});
        A.setDependencies(new Handler.Node[]{B, C, D});
        B.setDependencies(new Handler.Node[]{E,C});

        for(Handler.Node n : handler.priority(A))
        {
            System.out.println(n);
        }



    }
}
