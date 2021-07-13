package com.ey.pdf.annotate;

import org.apache.http.HttpHost;
import org.apache.http.auth.AuthScope;
import org.apache.http.auth.UsernamePasswordCredentials;
import org.apache.http.client.CredentialsProvider;
import org.apache.http.impl.client.BasicCredentialsProvider;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.pdmodel.PDPage;
import org.apache.pdfbox.pdmodel.common.PDRectangle;
import org.apache.pdfbox.pdmodel.graphics.color.PDColor;
import org.apache.pdfbox.pdmodel.graphics.color.PDDeviceRGB;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotation;
import org.apache.pdfbox.pdmodel.interactive.annotation.PDAnnotationTextMarkup;
import org.elasticsearch.action.get.GetRequest;
import org.elasticsearch.action.get.GetResponse;
import org.elasticsearch.client.*;

import java.io.*;
import java.util.List;
import java.util.Map;

import static com.ey.pdf.annotate.Config.*;

public class Application {

    public static void main(String [] args) throws IOException {
        File file = new File("src/main/resources/Input Sample.pdf");
        PDDocument doc = PDDocument.load(file);

        RestHighLevelClient client = createESRestClient();
        GetRequest getRequest = new GetRequest(
                INDEX,
                ID);

        GetResponse getResponse = client.get(getRequest, RequestOptions.DEFAULT);
        System.out.println(getResponse.toString());
        Map<String, Object> source = getResponse.getSource();

        for(Map.Entry<String,Object> item : source.entrySet()){
            PDPage page = doc.getPage(Integer.parseInt(item.getKey()));
            List<PDAnnotation> pageAnnotation = page.getAnnotations();

            //generate instance for annotation

            List<Map<String, String>> params = (List<Map<String, String>>) item.getValue();
            for(Map<String, String> param: params){
                PDAnnotationTextMarkup pageTxtMark = new PDAnnotationTextMarkup(PDAnnotationTextMarkup.SUB_TYPE_HIGHLIGHT);

                PDRectangle position = new PDRectangle();
                position.setLowerLeftX(Float.parseFloat(param.get("X1")));
                position.setLowerLeftY(Float.parseFloat(param.get("Y1")));
                position.setUpperRightX(Float.parseFloat(param.get("X2")));
                position.setUpperRightY(Float.parseFloat(param.get("Y2")));

                pageTxtMark.setRectangle(position);

                //set the quadpoint
                float[] quads = new float[8];
                //x1,y1
                quads[0] = position.getLowerLeftX();
                quads[1] = position.getUpperRightY()-1;
                //x2,y2
                quads[2] = position.getUpperRightX();
                quads[3] = quads[1];
                //x3,y3
                quads[4] = quads[0];
                quads[5] = position.getLowerLeftY()-1;
                //x4,y4
                quads[6] = quads[2];
                quads[7] = quads[5];
                pageTxtMark.setQuadPoints(quads);
                pageTxtMark.setContents(param.get("Element")+" : "+param.get("Error"));
                float[] components = new float[] {1, 1, 204 / 255F};
                PDColor pdColor = new PDColor(components, PDDeviceRGB.INSTANCE);

                pageTxtMark.setColor(pdColor);
                pageAnnotation.add(pageTxtMark);
                doc.save("new.pdf");
            }
        }
        client.close();
    }

    public static RestHighLevelClient createESRestClient() {
        Boolean esAuthentication = true;
        CredentialsProvider credentialsProvider = new BasicCredentialsProvider();
        credentialsProvider.setCredentials(AuthScope.ANY, new UsernamePasswordCredentials(USERNAME, PASSWORD));
        RestClientBuilder restClientBuilder = RestClient
                .builder(new HttpHost(HOSTNAME, PORT, "https"));
        // Use this one if your ElasticSearch server is setup to use username & password authentication
        if (esAuthentication) {
            restClientBuilder.setHttpClientConfigCallback(h -> h.setDefaultCredentialsProvider(credentialsProvider));
        }

        return new RestHighLevelClient(restClientBuilder);
    }
}
