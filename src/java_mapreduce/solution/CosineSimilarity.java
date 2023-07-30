package solution;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
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

        // private Map<String, RealVector> movieVectorMap = new HashMap<>();
        private Map<String, SparseVector> movieVectorMap = new HashMap<>();
        private Map<String, Double> magnitudeMap = new HashMap<>();
        private Set<String> combinationsSet = new HashSet<>();

        @Override
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            List<Integer> movieVector = new ArrayList<>();

            int magnitude = 0;
            for (IntWritable value: values){
                movieVector.add(value.get());
                magnitude += value.get() * value.get();
            }

            // RealVector vector = new ArrayRealVector(movieVector.stream().mapToDouble(Integer::doubleValue).toArray());
            SparseVector vector = new SparseVector(movieVector.size());
            for (int i = 0; i < movieVector.size(); i++) {
                if (movieVector.get(i) != 0){
                    vector.set(i, movieVector.get(i));
                }
            }

            movieVectorMap.put(key.toString(), vector);
            magnitudeMap.put(key.toString(), FastMath.sqrt(magnitude));
        }

        @Override
        protected void cleanup(Context context) throws IOException, InterruptedException {
            Map<String, Map<String, Double>> similarityMap = new ConcurrentHashMap<>();
            
            for (Map.Entry<String, RealVector> entry1 : movieVectorMap.entrySet()) {
                String movieTitle1 = entry1.getKey();
                // RealVector vector1 = entry1.getValue();
                SparseVector vector1 = entry1.getValue();
                double magnitude1 = magnitudeMap.get(movieTitle1);

                for (Map.Entry<String, RealVector> entry2 : movieVectorMap.entrySet()) {
                    String movieTitle2 = entry2.getKey();
                    // RealVector vector2 = entry2.getValue();
                    SparseVector vector2 = entry2.getValue();
                    double magnitude2 = magnitudeMap.get(movieTitle2);

                    if ((!movieTitle1.equals(movieTitle2)) && (!combinationsSet.contains(movieTitle1+","+movieTitle2) || !combinationsSet.contains(movieTitle2+","+movieTitle1))) {
                        double dotProduct = vector1.dotProduct(vector2);
                        double similarity = dotProduct / (magnitude1 * magnitude2);
                        context.write(new Text("("+movieTitle1+","+movieTitle2+")"), new DoubleWritable(similarity));
                        context.write(new Text("("+movieTitle2+","+movieTitle1+")"), new DoubleWritable(similarity));
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
