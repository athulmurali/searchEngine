import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.io.FileWriter;
import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.StringField;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */

/**
 * @author Sachin Haldavanekar
 * This program assumes that if the index folder is present then it should only 
 * perform a query operation else it should first index all files in source 
 * folder and then store indexes in index folder.
 * 
 * To completely index all files again, delete the index folder and run the 
 * program.
 */
public class HW4 {

	private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);
	private IndexWriter writer;
	private ArrayList<File> queue = new ArrayList<File>();

	/** Main function
	 *  
	 * @param - args
	 * 			args[0] - will contain path of the folder to store index in.
	 * 			args[1] - will contain path of the folder to get raw documents from.
	 *			All queries will be in the args and each word in a query will be
	 * 			delimited by the following symbol <-->
	 * 
	 * @throws IOException
	 * 			when exception occurs.
	 * **/
	public static void main(String[] args) throws IOException {

		String indexLocation = null;
		String sysUserDir = System.getProperty("user.dir") ;
		String s = args[0].equalsIgnoreCase("")? sysUserDir + "/index":args[0];
		File f = new File(s); 

		HW4 indexer = null;
		indexLocation = s;
		
		if (!f.exists()) {
			if (f.mkdir()) {
				try {
					indexer = new HW4(f);
				} catch (Exception ex) {
					System.out.println("Cannot create index..." + ex.getMessage());
					System.exit(-1);
				}
				// ===================================================
				// read input from user until he enters q for quit
				// ===================================================
				try {
					s = args[0].equalsIgnoreCase("")? sysUserDir + "/source":args[1];
					// try to add file into the index
					indexer.indexFileOrDirectory(s);
				} catch (Exception e) {
					System.out.println("Error indexing " + s + " : "
							+ e.getMessage());
				}
				indexer.closeIndex();
			}
		}

		// ===================================================
		// after adding, we always have to call the
		// closeIndex, otherwise the index is not created
		// ===================================================
		

		// =========================================================
		// Now search
		// =========================================================
		IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
				indexLocation)));
		IndexSearcher searcher = new IndexSearcher(reader);
		TopScoreDocCollector collector;

		File docFile = new File("Doc_score.txt");
		FileWriter docFileWriter = new FileWriter(docFile);

		for(int i = 2; i <= args.length; i++)	{
			try {
				String Qid = args[i].split(":")[0];
				String delimiter = "<-->";
				String spaceBar = " ";
				String input_query = args[i].split(":")[1].replace(delimiter,spaceBar);
				Query q = new QueryParser(
						Version.LUCENE_47, 
						"contents", 
						analyzer).parse(
								input_query.toLowerCase());
				collector = TopScoreDocCollector.create(1000, true);
				searcher.search(q, collector);
				ScoreDoc[] hits = collector.topDocs().scoreDocs;

				// 4. display results
				System.out.println("Found " + hits.length + " hits.");
				for (int j = 0; j < Math.min(100, hits.length); ++j) {
					int docId = hits[j].doc;
					Document d = searcher.doc(docId);
					String filename = d.get("filename");
					filename = filename.substring(0, filename.length() - 4);
					String concatenatedOutput =
							Qid + " Q0" + 
									" " +  filename +
									"\t" + (j + 1) +  
									"\t" + hits[j].score + 
									"\tLucene" +
									System.lineSeparator();
					System.out.print(concatenatedOutput);
					docFileWriter.write(concatenatedOutput);
				}

				docFileWriter.write("\n\n");
				Qid = "";
				input_query = "";
			}
			catch(Exception e){
				System.exit(-1);
			}
		}
		docFileWriter.close();
	}

	/**
	 * Constructor
	 * 
	 * @param indexDir
	 *            the name of the folder in which the index should be created
	 * @throws java.io.IOException
	 *             when exception creating index.
	 */
	HW4(File f) throws IOException {

		FSDirectory dir = FSDirectory.open(f);

		IndexWriterConfig config = new IndexWriterConfig(Version.LUCENE_47,
				analyzer);

		writer = new IndexWriter(dir, config);
	}

	/**
	 * Indexes a file or directory
	 * 
	 * @param fileName
	 *            the name of a text file or a folder we wish to add to the
	 *            index
	 * @throws java.io.IOException
	 *             when exception
	 */
	public void indexFileOrDirectory(String fileName) throws IOException {
		// ===================================================
		// gets the list of files in a folder (if user has submitted
		// the name of a folder) or gets a single file name (is user
		// has submitted only the file name)
		// ===================================================
		addFiles(new File(fileName));

		int originalNumDocs = writer.numDocs();
		for (File f : queue) {
			FileReader fr = null;
			try {
				Document doc = new Document();

				// ===================================================
				// add contents of file
				// ===================================================
				fr = new FileReader(f);
				doc.add(new TextField("contents", fr));
				doc.add(new StringField("path", f.getPath(), Field.Store.YES));
				doc.add(new StringField("filename", f.getName(),
						Field.Store.YES));

				writer.addDocument(doc);
				System.out.println("Added: " + f);
			} catch (Exception e) {
				System.out.println("Could not add: " + f);
			} finally {
				fr.close();
			}
		}

		int newNumDocs = writer.numDocs();
		System.out.println("");
		System.out.println("************************");
		System.out.println((newNumDocs - originalNumDocs) + " documents added.");
		System.out.println("************************");

		queue.clear();
	}

	private void addFiles(File file) { 

		if (!file.exists()) {
			System.out.println(file + " does not exist.");
		}
		if (file.isDirectory()) {
			for (File f : file.listFiles()) {
				addFiles(f);
			}
		} else {
			String filename = file.getName().toLowerCase();
			// ===================================================
			// Only index text files
			// ===================================================
			if (filename.endsWith(".htm") || filename.endsWith(".html")
					|| filename.endsWith(".xml") || filename.endsWith(".txt")) {
				queue.add(file);
			} else {
				System.out.println("Skipped " + filename);
			}
		}
	}

	/**
	 * Close the index.
	 * 
	 * @throws java.io.IOException
	 *             when exception closing
	 */
	public void closeIndex() throws IOException {
		writer.close();
	}
}