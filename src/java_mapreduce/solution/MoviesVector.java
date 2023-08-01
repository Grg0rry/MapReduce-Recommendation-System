package solution;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.URI;
import java.util.HashMap;
import java.util.Map;


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
  public static class MoviesVectorReducer extends Reducer<Text, Text, Text, Text> {
    
    private Map<Integer, Integer> read_userRatings;

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
      // Goes through the additional UserList and Store into a Map for later processing
      read_userRatings = new HashMap<>();

      URI[] cacheFiles = context.getCacheFiles();
      Path cachedFilePath = new Path(cacheFiles[0]);
      try (BufferedReader reader = new BufferedReader(new InputStreamReader(FileSystem.get(context.getConfiguration()).open(cachedFilePath)))) {
        String line;
        while ((line = reader.readLine()) != null) {
          String[] tokens = line.split("\t", 2);
          read_userRatings.put(Integer.parseInt(tokens[1]), 0);
        }
      }
    }

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      Map<Integer, Integer> write_userRatings = new HashMap<>(read_userRatings);
      StringBuffer strblder = new StringBuffer();

      // Create the vector for each movie
      for (Text userRating : values) {
        String[] UserRating = userRating.toString().split(":");
        int userID = Integer.parseInt(UserRating[0]);
        int rating = Integer.parseInt(UserRating[1]);

        write_userRatings.put(userID, rating);
      }

      for (Integer rating: write_userRatings.values()){
        strblder.append("," + rating);
      }

      context.write(key, new Text(strblder.toString().replaceFirst(",", "")));
    }
  }

  /* Driver */
  public static void main(String[] args) throws Exception {
    
    // Create a new MapReduce job
    Job job = new Job();

    // Set the job configuration
    job.setJarByClass(MoviesVector.class);
    job.setJobName("MoviesVector");
    
    // Set the input and output paths and Additional file
    job.addCacheFile(new Path(args[0]).toUri());
    FileInputFormat.setInputPaths(job, new Path(args[1]));
    FileOutputFormat.setOutputPath(job, new Path(args[2]));

    // Set the Mapper and Reducer classes
    job.setMapperClass(MoviesVectorMapper.class);
    job.setReducerClass(MoviesVectorReducer.class);

    // Set the expected key and value types
    job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    
    // Wait for the job to complete and then exit
    job.waitForCompletion(true);
  }
}