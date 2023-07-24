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
  public static class MoviesVectorMapper extends Mapper<Object, Text, Text, List<Pair>> {
    
    private List<Integer> userList;

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
      userList = new ArrayList<>();
      Path[] cacheFiles = context.getLocalCacheFiles();

      try (BufferedReader reader = new BufferedReader(new FileReader(cacheFiles[0].toString()))) {
        String line;
        while ((line = reader.readLine()) != null) {
          String[] tokens = line.split("\t", 2);
          userList.add(Integer.parseInt(tokens[1]));
        }
      }
    }
    
    @Override
    public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
      String[] line = value.toString().split("\t", 2);

      String movieTitle = line[0];
      List<Pair> userRatings = new ArrayList<>();
      for (String ratingPair : line[1].split(",")){
        String[] rating = ratingPair.split(":");
        userRatings.add(new Pair(Integer.parseInt(rating[0]), Integer.parseInt(rating[1])));
      }
      
      if (userRatings.size() >= 1000) {
        context.write(new Text(movieTitle), userRatings);
      }
    }
  }

  /* Reducer */
  public static class MoviesVectorReducer extends Reducer<Text, List<Pair>, Text, List<Integer>> {

    private Map<Integer, Integer> userRatingsByOrder;

    @Override
    protected void setup(Context context) throws IOException, InterruptedException {
      userRatingsByOrder = new HashMap<>();
    }

    @Override
    public void reduce(Text key, Iterable<List<Pair>> values, Context context) throws IOException, InterruptedException {
      userRatingsByOrder.clear();

      for (List<Pair> userRatings : values) {
        for (Pair userRating: userRatings) {
          Integer userID = userRating.userID;
          Integer rating = userRating.rating;

          if (userID != null && rating != null) {
            userRatingsByOrder.put(userID, rating);
          }
        }
      }

      List<Integer> vector = new ArrayList<>(userRatingsByOrder.values());
      context.write(key, vector);
    }

    @Override
    public void cleanup(Context context) throws IOException, InterruptedException {
      super.cleanup(context);
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
		job.setMapOutputValueClass(List.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(List.class);
          
    job.waitForCompletion(true);
  }
}

class Pair {
  public Integer userID;
  public Integer rating;

  public Pair(Integer userID, Integer rating){
    this.userID = userID;
    this.rating = rating;
  }
}