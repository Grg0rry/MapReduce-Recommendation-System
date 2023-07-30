package solution;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Vector;
import java.util.concurrent.ConcurrentHashMap;

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

        private Map<String, RealVector> movieVectorMap = new HashMap<>();
        private Map<String, Double> magnitudeMap = new HashMap<>();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            List<Integer> movieVector = new ArrayList<>();

            int magnitude = 0;
            for (IntWritable value: values){
                movieVector.add(value.get());
                magnitude += value.get() * value.get();
            }

            RealVector vector = new ArrayRealVector(movieVector.stream().mapToDouble(Integer::doubleValue).toArray());
            movieVectorMap.put(key.toString(), vector);
            magnitudeMap.put(key.toString(), FastMath.sqrt(magnitude));
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            Map<String, Map<String, Double>> similarityMap = new ConcurrentHashMap<>();
            
            for (Map.Entry<String, RealVector> entry1 : movieVectorMap.entrySet()) {
                String movieTitle1 = entry1.getKey();
                RealVector vector1 = entry1.getValue();
                double magnitude1 = magnitudeMap.get(movieTitle1);

                for (Map.Entry<String, RealVector> entry2 : movieVectorMap.entrySet()) {
                    String movieTitle2 = entry2.getKey();
                    RealVector vector2 = entry2.getValue();
                    double magnitude2 = magnitudeMap.get(movieTitle2);

                    if (!movieTitle1.equals(movieTitle2)) {
                        double dotProduct = vector1.dotProduct(vector2);
                        double similarity = dotProduct / (magnitude1 * magnitude2);

                        similarityMap.computeIfAbsent(movieTitle1, k -> new HashMap<>()).put(movieTitle2, similarity);
                        similarityMap.computeIfAbsent(movieTitle2, k -> new HashMap<>()).put(movieTitle1, similarity);
                    }
                }
            }

            for (Map.Entry<String, Map<String, Double>> entry : similarityMap.entrySet()){
                String movieTitle = entry.getKey();
                Map<String, Double> similarity = entry.getValue();
                
                context.write(new Text("(" + movieTitle + "," + similarity.keySet().iterator().next() + ")"), new DoubleWritable(similarity.values().stream().max(Double::compareTo).get()));
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
		job.setMapOutputValueClass(IntWritable.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(DoubleWritable.class);

        job.waitForCompletion(true);
    }
}
