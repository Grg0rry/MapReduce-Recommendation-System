package solution;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.io.ArrayWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;


public class MoviesVector {

  /* Mapper */
  public static class MoviesVectorMapper extends Mapper<LongWritable, Text, Text, Text> {
    
    @Override
    public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
      String[] line = value.toString().trim().split("\t", 2);
      
      for (String userRating: line[1].split(",")){
        context.write(new Text(line[0]), new Text(userRating));
      }
    }
  }

  /* Reducer */
  public static class MoviesVectorReducer extends Reducer<Text, Text, Text, ArrayWritable> {

    private Map<Integer, Integer> userRatingsByOrder;
    private Map<Integer, Integer> temp_userRatingsByOrder;

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
      userRatingsByOrder = new HashMap<>();

      try (BufferedReader reader = new BufferedReader(new FileReader(context.getCacheFiles()[0].toString()))) {
        String line;
        while ((line = reader.readLine()) != null) {
          String[] tokens = line.split("\t", 2);
          userRatingsByOrder.put(Integer.parseInt(tokens[1]), 0);
        }
      }
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      temp_userRatingsByOrder = new HashMap<>(userRatingsByOrder);

      for (String UserRating: values){
        String[] rating = UserRating.split(":");
        temp_userRatingsByOrder.put(Integer.parseInt(rating[0]), Integer.parseInt(rating[1]));
      }

      List<Integer> vector = new ArrayList<>(temp_userRatingsByOrder.values());
      context.write(key, new ArrayWritable(IntWritable.class, vector));
    }
  }

  /* Driver */
  public static void main(String[] args) throws Exception {
      
    Job job = new Job();

    job.setJarByClass(MoviesVector.class);
    job.setJobName("MoviesVector");
    
    job.addCacheFile(new Path(args[0]).toUri());
    FileInputFormat.setInputPaths(job, new Path(args[1]));
    FileOutputFormat.setOutputPath(job, new Path(args[2]));

    job.setMapperClass(MoviesVectorMapper.class);
    job.setReducerClass(MoviesVectorReducer.class);

    job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(ArrayWritable.class);
          
    job.waitForCompletion(true);
  }
}