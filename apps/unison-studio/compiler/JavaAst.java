// Trusted GLASS adapter: JavacTask.parse() parses, never compiles or executes supplied Java.
// Java source-file execution runs *this parser program*, not the untrusted source string.
import javax.tools.*;
import com.sun.source.util.*;
import com.sun.source.tree.*;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.util.*;

public final class JavaAst {
 static class MemorySource extends SimpleJavaFileObject {
   final String code;
   MemorySource(String value){ super(URI.create("string:///GLASSSource.java"),JavaFileObject.Kind.SOURCE);code=value; }
   @Override public CharSequence getCharContent(boolean ignoreEncodingErrors){return code;}
 }
 static class Scanner extends TreeScanner<Void,Void> {
   final List<String> nodes=new ArrayList<>();
   final List<String> stack=new ArrayList<>();
   String escape(String s){StringBuilder b=new StringBuilder("\"");for(char c:s.toCharArray()){
     if(c=='"'||c=='\\')b.append('\\').append(c);
     else if(c<32)b.append(String.format("\\u%04X",(int)c));
     else b.append(c);
   }return b.append('"').toString();}
   @Override public Void scan(Tree tree, Void ignored){
     if(tree==null)return null;
     if(nodes.size()>=640||stack.size()>=80)throw new IllegalArgumentException("node/depth budget exceeded");
     String id=String.format("n%04d",nodes.size());
     String kind=tree.getKind().toString();
     String label="";
     if(tree instanceof ClassTree t)label=t.getSimpleName().toString();
     else if(tree instanceof MethodTree t)label=t.getName().toString();
     else if(tree instanceof VariableTree t)label=t.getName().toString();
     else if(tree instanceof IdentifierTree t)label=t.getName().toString();
     else if(tree instanceof MemberSelectTree t)label=t.getIdentifier().toString();
     else if(tree instanceof ImportTree t)label=t.getQualifiedIdentifier().toString();
     if(label.length()>100)label=label.substring(0,100);
     String parent=stack.isEmpty()?"null":escape(stack.get(stack.size()-1));
     nodes.add("{\"kind\":"+escape(kind)+",\"label\":"+escape(label)+",\"parent\":"+parent+",\"span\":null}");
     stack.add(id);super.scan(tree,ignored);stack.remove(stack.size()-1);return null;
   }
 }
 public static void main(String[] args) throws Exception {
   byte[] input=System.in.readNBytes(32769);
   if(input.length>32768)throw new IllegalArgumentException("source budget exceeded");
   String source=new String(input,StandardCharsets.UTF_8);
   var compiler=ToolProvider.getSystemJavaCompiler();
   if(compiler==null)throw new IllegalStateException("JDK compiler unavailable");
   var diagnostics=new DiagnosticCollector<JavaFileObject>();
   try(var fm=compiler.getStandardFileManager(diagnostics,null,StandardCharsets.UTF_8)){
     var task=(JavacTask)compiler.getTask(null,fm,diagnostics,List.of("-proc:none"),null,List.of(new MemorySource(source)));
     var scanner=new Scanner();
     for(var tree:task.parse())scanner.scan(tree,null);
     if(diagnostics.getDiagnostics().stream().anyMatch(d->d.getKind()==Diagnostic.Kind.ERROR)){
       throw new IllegalArgumentException("Java parser diagnostics contain errors");
     }
     System.out.println("{\"parser\":\"JDK JavacTask.parse Java syntax tree\",\"nodes\":["+String.join(",",scanner.nodes)+"]}");
   }
 }
}
