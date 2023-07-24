package solution;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map;
import java.util.ArrayList;
import java.util.List;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;


public class MoviesVector extends Configured implements Tool {

  /* Mapper */
  public static class MoviesVectorMapper extends Mapper<Object, Text, Text, Text> {
    
    private Map<Integer, Integer> userMap;

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
      super.setup(context);
      userMap = new HashMap<>();

      Path[] cacheFiles = context.getLocalCacheFiles();
      if (cacheFiles != null && cacheFiles.length > 0){
        try (BufferedReader br = new BufferedReader(new FileReader(cacheFiles[0].toString()))) {
          String line:
          while ((line = br.readLine()) != null) {
            String[] parts = line.split("\t", 2);
            if (parts.length == 2) {
              int userID = Integer.parseInt(parts[0]);
              int order = Integer.parseInt(parts[1]);
              userMap.put(order, userID);
            }
          }
        }
      }
    }
    
    @Override
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String[] line = value.toString().split("\t", 2);
      String movieTitle = line[0];
      String userRatingStr = line[1];
      String[] userRatingsArray = userRatingsStr.substring(1, userRatingsStr.length() - 1).split(", ");
      List<String> userRatingPairs = new ArrayList<>();

      for (String pair : userRatingsArray){
        String[] parts = pair.split(":");
        int order = Integer.parseInt(parts[0]);
        int rating = Integer.parseInt(parts[1]);
        int userId = userMap.getOrDefault(order, -1);

        if (userId != -1) {
          userRatingPairs.add(userId + ":" + rating);
        }
      }

      if (userRatingPairs.size() >= 1000) {
        context.write(new Text(movieTitle), new Text(userRatingPairs.toString()));
      }    
    }
  }

  /* Reducer */
  public static class MoviesVectorReducer extends Reducer<Text, Text, Text, Text> {

    @Override
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      Map<Integer, Integer> userRatingsByOrder = new HashMap<>();
      
      for (Text value : values) {
        String userRatingsStr = value.toString();
        String[] userRatingsArray = userRatingsStr.substring(1, userRatingsStr.length() - 1).split(", ");
        for (String pair : userRatingsArray) {
          String[] parts = pair.split(":");
          int userId = Integer.parseInt(parts[0]);
          int rating = Integer.parseInt(parts[1]);
          userRatingsByOrder.put(userId, rating);
        }
      }

      List<Integer> vector = new ArrayList<>();
      for (int userId : userRatingsByOrder.keySet()) {
        vector.add(userRatingsByOrder.get(userId));
      }

      context.write(key, new Text(vector.toString()));
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
    job.setOutputValueClass(Text.class);
          
    job.waitForCompletion(true);
  }
}