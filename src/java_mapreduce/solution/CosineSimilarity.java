import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import org.nd4j.linalg.api.ndarray.INDArray;
import org.nd4j.linalg.factory.Nd4j;


public class CosineSimilarity extends Configured implements Tool {

    /* Mapper */
    public static class CosineSimilarityMapper extends Mapper<LongWritable, Text, Text, IntWritable> {

        @Override
        public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            
            String[] line = value.toString().trim().split("\t", 2);

            String movieTitle = line[0];
            String[] ratingsArray = line[1].split(",");

            for (String rating : ratingsArray) {
                context.write(new Text(movieTitle), new IntWritable(Integer.parseInt(rating)));
            }
        }
    }

    /* Reducer */
    public static class CosineSimilarityReducer extends Reducer<Text, IntWritable, Text, DoubleWritable> {

        private Map<String, List<Integer>> movieVectorMap = new HashMap<>();
        private Map<String, Double> magnitudeMap = new HashMap<>();

        @Override
        protected void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            List<Integer> movieVector = new ArrayList<>();

            for (IntWritable value: values){
                movieVector.add(value.get());
            }
            movieVectorMap.put(key, movieVector);

            double magnitude = Nd4j.create(movieVector).norm2Number().doubleValue();
            magnitudeMap.put(key, magnitude);
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            for (Map.Entry<String, List<Integer>> entry1 : movieVectorMap.entrySet()) {
                String movieTitle1 = entry1.getKey();
                INDArray vector1 = Nd4j.create(entry1.getValue());
                double magnitude1 = magnitudeMap.get(movieTitle1);
                
                for (Map.Entry<String, List<Integer>> entry2 : movieVectorMap.entrySet()) {
                    String movieTitle2 = entry2.getKey();
                    INDArray vector2 = Nd4j.create(entry2.getValue());
                    double magnitude2 = magnitudeMap.get(movieTitle2);
                    
                    double dotProduct = vector1.mmul(vector2.transpose()).getDouble(0, 0);
                    double similarity = dotProduct / (magnitude1 * magnitude2);
                    context.write(new Text(movieTitle1.toString()+","+movieTitle2.toString()), new DoubleWritable(similarity));
                }
            }
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
        
        job.setJarByClass(CosineSimilarity.class);
        job.setJobName("CosineSimilarity");

        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        job.setMapperClass(CosineSimilarityMapper.class);
        job.setReducerClass(CosineSimilarityReducer.class);

        job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(Text.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        job.waitForCompletion(true);
    }
}
