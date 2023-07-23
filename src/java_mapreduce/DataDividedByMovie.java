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

      if (items.length >= 3) {
        int UserID = Integer.parseInt(items[1]);
        String MovieTitle = items[0];
        int Rating = Integer.parseInt(items[2]);

        context.write(new Text(MovieTitle), new Text(UserID + ':' + Rating));
      }
    }
  }

  /* Reducer */
  public static class DataDividedByMovieReducer extends Mapper<Text, Text, Text, Text> {

    @Override
    public void map(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {

      StringBuilder UserRating_lst = new StringBuilder();
      while (values.iterator().hasNext()){
        UserRating_lst.append(',' + values.iterator().next());
      }

      context.write(key, new Text(UserRating_lst.toString().replaceFirst(",", "")));
    }
  }

  /* Driver */
  public static void main(String[] args) throws Exception {

    if (args.length != 2) {
      System.out.printf(
        "Usage: MapReduce <input dir> <output dir>\n");
      System.exit(-1);
    }
      
    Job job = new Job();

    job.setJarByClass(DataDividedByMovie.class);
    job.setJobName("DataDividedByMovie");
      
    FileInputFormat.setInputPaths(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path(args[1]));

    job.setMapperClass(DataDividedByMovieMapper.class);
    job.setReducerClass(DataDividedByMovieReducer.class);

    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);

    job.waitForCompletion(true);
  }
}