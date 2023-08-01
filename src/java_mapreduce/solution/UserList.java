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


public class UserList {
  
  /* Mapper */
  public static class UserListMapper extends Mapper<LongWritable, Text, IntWritable, Text> {

    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {

      String[] items = value.toString().trim().split(",", 3);

      // Ensure it has min 3 elements
      if (items.length >= 3) {
        int UserID = Integer.parseInt(items[1]);

        context.write(new IntWritable(UserID), new Text(""));
      }
    }
  }

  /* Reducer */
  public static class UserListReducer extends Reducer<IntWritable, Text, Text, IntWritable> {

    @Override
    public void reduce(IntWritable key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      
      // Emits with the $User_List
      context.write(new Text("$User_List"), key);
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
    job.setJarByClass(UserList.class);
    job.setJobName("UserList");
    
    // Set the input and output paths
    FileInputFormat.setInputPaths(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    // Set the Mapper and Reducer classes
    job.setMapperClass(UserListMapper.class);
    job.setReducerClass(UserListReducer.class);
    
    // Set the expected key and value types
    job.setMapOutputKeyClass(IntWritable.class);
		job.setMapOutputValueClass(Text.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    
    // Wait for the job to complete and then exit
    job.waitForCompletion(true);
  }
}