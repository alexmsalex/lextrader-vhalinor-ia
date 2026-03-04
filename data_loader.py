import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;

public class DataLoader {

    public static void main(String[] args) {
        String csvFilePath = "path_to_your_csv_file.csv";
        String apiUrl = "https://api.example.com/data";

        try {
            loadCSV(csvFilePath);
        } catch (IOException e) {
            System.out.println("Erro ao carregar dados do arquivo " + csvFilePath + ": " + e.getMessage());
        }

        try {
            loadDataFromAPI(apiUrl);
        } catch (IOException e) {
            System.out.println("Erro ao carregar dados da API " + apiUrl + ": " + e.getMessage());
        }
    }

    public static void loadCSV(String filePath) throws IOException {
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            CSVParser parser = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(br);
            for (CSVRecord record : parser) {
                // Process each record
                System.out.println("Record: " + record);
            }
            System.out.println("Dados carregados do arquivo " + filePath);
        }
    }

    public static void loadDataFromAPI(String apiUrl) throws IOException {
        URL url = new URL(apiUrl);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("GET");

        try (BufferedReader br = new BufferedReader(new InputStreamReader(conn.getInputStream()))) {
            CSVParser parser = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(br);
            for (CSVRecord record : parser) {
                // Process each record
                System.out.println("Record: " + record);
            }
            System.out.println("Dados carregados da API " + apiUrl);
        } catch (IOException e) {
            System.out.println("Erro ao carregar dados da API " + apiUrl + ": " + e.getMessage());
            throw e;
        }
    }
}
