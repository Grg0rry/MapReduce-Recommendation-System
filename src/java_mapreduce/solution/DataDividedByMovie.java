package solution;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper;
import java.io.IOException;


public class DataDividedByMovie {

  /* Mapper */
  public static class DataDividedByMovieMapper extends Mapper<LongWritable, Text, Text, Text> {

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

      String line = value.toString().trim();
      String [] items = line.split(",", 3);

      // Ensure it has min 3 elements
      if (items.length >= 3) {
        int UserID = Integer.parseInt(items[1]);
        String MovieTitle = items[0];
        int Rating = Integer.parseInt(items[2]);

        context.write(new Text(MovieTitle), new Text(String.valueOf(UserID) + ':' + String.valueOf(Rating)));
      }
    }
  }

  /* Reducer */
  public static class DataDividedByMovieReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      
      // Convert the list of values to string
      StringBuilder strblder = new StringBuilder();
      while (values.iterator().hasNext()){
        strblder.append("," + values.iterator().next());
      }
      
      context.write(key, new Text(strblder.toString().replaceFirst(",","")));
    }
  }

  /* Driver */
  public static void main(String[] args) throws Exception {
    if (args.length != 2) {
      System.out.printf(
        "Usage: MapReduce <input dir> <output dir>\n");
      System.exit(-1);
    }
    
    // Create a new MapReduce job
    Job job = new Job();

    // Set the job configuration
    job.setJarByClass(DataDividedByMovie.class);
    job.setJobName("DataDividedByMovie");
    
    // Set the input and output paths
    FileInputFormat.setInputPaths(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    // Set the Mapper and Reducer classes
    job.setMapperClass(DataDividedByMovieMapper.class);
    job.setReducerClass(DataDividedByMovieReducer.class);
    
    // Set the expected key and value types
    job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    // Wait for the job to complete and then exit
    job.waitForCompletion(true);
  }
}