
## Frequently Asked Questions (FAQ)

### General Questions

**Q1: What does the Triton Llama repository do?**

-   **A:**  It helps users set up transformer models on NVIDIA's Triton Inference Server, including tools for converting models to ONNX format and setting up monitoring with Prometheus, Grafana, and Loki.

**Q2: What do I need before using this repository?**

-   **A:**  You need Docker, Docker Compose, and Python on your computer. Knowing basic Docker and ONNX model handling is helpful.

### Setup and Configuration

**Q3: How do I start using this setup?**

-   **A:**  Run the  `bash scripts/up.sh`  script in the main directory of the repository. This script prepares everything automatically.

**Q4: How do I make sure my model works with Triton?**

-   **A:**  Convert your model to ONNX format and check the  `config.pbtxt`  file to match the model’s input and output setup. Triton supports many formats, so make sure to convert properly for Torchscript and tensor flow.

### Using Triton Server

**Q5: How do I use the Triton server after setting it up?**

-   **A:**  Use HTTP/GRPC requests to interact with the server. The Python script  `test-triton.py`  in the  `demo`  folder is a good example of how to do this.

### Monitoring and Troubleshooting

**Q6: How do I look at the monitoring tools like Prometheus and Grafana?**

-   **A:**  Access Prometheus at  `http://localhost:9090`  and Grafana at  `http://localhost:3000`. Log in with the default credentials or ones you set to see the dashboards.

**Q7: What should I do if the model isn't working right?**

-   **A:**  Check the model's activity in Grafana for any errors. Make sure the model inputs are correct and the model is getting the right data.

**Q8: How do I update a model or its settings in Triton?**

-   **A:**  Change the model files or the  `config.pbtxt`  file as needed and restart the Triton server to apply updates.

**Q9: Can I increase the Triton server's capacity for more traffic?**

-   **A:**  Yes, you can scale up the server. Increase the number of server instances in the  `docker-compose.yml`  file by changing the  `replicas`  setting.

### Adding a New Model to Triton

1.  **Prepare the Model**: Make sure your new model is ready for Triton, in ONNX, TensorFlow, or TorchScript format.
2.  **Place the Model**: Create a folder in the  `models`  directory for your new model. For example, make  `models/NewModel/`  and put your model files there.
3.  **Update the Configuration**: Make a new  `config.pbtxt`  file in the new model's directory. Set it up to match your model’s needs.
4.  **Adjust the Script**: Read and adapt  `scripts/up.sh`  to set up models, update it to handle your new model.
5.  **Restart Triton Server**: Turn off and start the server again to load the new model.

### Client-Side Operations

**Why handle some tasks on the client side?**

-   **To Reduce Server Load**: Doing tasks like database interactions and token handling on the client side keeps the server focused on model inference.
-   **To Use Client Resources**: Clients often have spare capacity to handle pre and post-inference tasks efficiently.
-   **To Scale Better**: Separating tasks allows client machines to share the workload, making the system more scalable.

### Monitoring and Enhancing Model Performance

**How do we monitor and improve models?**

-   **Using Infra Monitoring Tools**: Use Prometheus for tracking server metrics and Grafana for visual monitoring. Loki helps manage logs.
-   **Logging to PostgreSQL**: A PostgreSQL database logs each model inference, storing both input and output, which helps analyze the model's performance over time. Additionally other data points like attention weights can be retrieved from the triton deployed model and logged to the database.

**How does this help improve training data?**

-   **Identifying Patterns**: By reviewing logged data, you can spot common issues or patterns. This information can help improve how the model responds or enhance the training data to cover gaps in knowledge.