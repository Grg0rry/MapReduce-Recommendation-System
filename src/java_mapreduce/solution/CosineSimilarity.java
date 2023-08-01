package solution;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.Vector;

import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import org.apache.commons.math3.linear.ArrayRealVector;
import org.apache.commons.math3.linear.RealVector;
import org.apache.commons.math3.util.FastMath;


public class CosineSimilarity {

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

        // To store movie vectors, magnitude, and combinations
        private Map<String, RealVector> movieVectorMap = new HashMap<>();
        private Map<String, Double> magnitudeMap = new HashMap<>();
        private Set<String> combinationsSet = new HashSet<>();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            List<Integer> movieVector = new ArrayList<>();
            
            // Compute the magnitude and movie vector
            int magnitude = 0;
            for (IntWritable value: values){
                movieVector.add(value.get());
                magnitude += value.get() * value.get();
            }

            // Convert the list of ratings to a real vector
            RealVector vector = new ArrayRealVector(movieVector.stream().mapToDouble(Integer::doubleValue).toArray());
            movieVectorMap.put(key.toString(), vector);
            magnitudeMap.put(key.toString(), FastMath.sqrt(magnitude));
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {       
            // Iterate over all movie pairs and calculate cosine similarity
            for (Map.Entry<String, RealVector> entry1 : movieVectorMap.entrySet()) {
                for (Map.Entry<String, RealVector> entry2 : movieVectorMap.entrySet()) {
                    String movieTitle1 = entry1.getKey();
                    String movieTitle2 = entry2.getKey();
                    if ((!movieTitle1.equals(movieTitle2)) && (!combinationsSet.contains(movieTitle1+","+movieTitle2) || !combinationsSet.contains(movieTitle2+","+movieTitle1))) {
                        
                        RealVector vector1 = entry1.getValue();
                        double magnitude1 = magnitudeMap.get(movieTitle1);
                        RealVector vector2 = entry2.getValue();
                        double magnitude2 = magnitudeMap.get(movieTitle2);

                        // Calculate dot product and cosine similarity
                        double dotProduct = vector1.dotProduct(vector2);
                        double similarity = dotProduct / (magnitude1 * magnitude2);

                        context.write(new Text("("+movieTitle1+","+movieTitle2+")"), new DoubleWritable(similarity));
                        context.write(new Text("("+movieTitle2+","+movieTitle1+")"), new DoubleWritable(similarity));

                        // Mark the MovieTitle pair to avoid duplicates
                        combinationsSet.add(movieTitle1+","+movieTitle2);
                        combinationsSet.add(movieTitle2+","+movieTitle1);
                    }
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

        // Create a new MapReduce job
        Job job = new Job();
        
        // Set the job configuration
        job.setJarByClass(CosineSimilarity.class);
        job.setJobName("CosineSimilarity");

        // Set the input and output paths
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        // Set the Mapper and Reducer classes
        job.setMapperClass(CosineSimilarityMapper.class);
        job.setReducerClass(CosineSimilarityReducer.class);

        // Set the expected key and value types
        job.setMapOutputKeyClass(Text.class);
		job.setMapOutputValueClass(IntWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        // Wait for the job to complete and then exit
        job.waitForCompletion(true);
    }
}
