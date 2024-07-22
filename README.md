# Chat With Your PDF

This application allows users to chat with their PDF documents using AI. It uses a a vector store and OpenAI's language models for text processing and generation. It provides the option to use a local vector store (FAISS) or a SAP HANA database.

## Features

- PDF upload and processing
- AI-powered chat interface for asking questions about the PDF content

## Prerequisites

- SAP AI Core service instance (with Extended service plan) and service key
- [Python](https://www.python.org/downloads/)
- (Optionally) [Git](https://git-scm.com/downloads)
- (Optionally) [Visual Studio Code](https://code.visualstudio.com/download)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/klemensfabian/chat-with-your-pdf
   ```
   Optionally: Download as zip file

2. Create a virtual environment and activate it:
   ```
   cd pdf-chat-app
   python -m venv venv
   .\venv\Scripts\activate # On Windows
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   Create a `.env` file in the project root and add the following informations:
   ```
   # AI Core
   AICORE_BASE_URL=your-aicore-baseurl + "/v2"
   AICORE_AUTH_URL=your-aicore-auth-url + "/oauth/token"
   AICORE_CLIENT_ID=your-aicore-client-id
   AICORE_CLIENT_SECRET=your-aicore-client-secret
   AICORE_RESOURCE_GROUP="default"
   # HANA DB (optional)
   SAP_HANA_ADDRESS=your-sap-hana-address
   SAP_HANA_PORT=your-sap-hana-port # usually 443
   SAP_HANA_USER=your-sap-hana-username
   SAP_HANA_PASSWORD=your-sap-hana-password
   ```
   #### AI Core
   The AI Core information can be found in the BTP Cockpit under Service Keys for your AI Core instance.
   Note: You need an AI Core Extended plan to access generative AI models.
   Alternative for .env: You can copy your secret key to `~/.aicore/config.json` or use `aicore configure` to set the config file, see https://pypi.org/project/ai-core-sdk/.
   #### HANA Vector DB
   This is optional. If you do not have access to a HANA DB you can use a local vector store. Here we use [FAISS](https://github.com/facebookresearch/faiss).
6. Run the application:
   ```
   streamlit run main.py
   ```

## Usage

1. Upload a PDF file using the drag-and-drop interface or file selector.
2. Once the PDF is processed, you can start asking questions about its content.

## Links
- [Generative AI Hub SDK](https://github.wdf.sap.corp/AI/generative-ai-hub-sdk)
- [Langchain](https://www.langchain.com/)
- [SAP HANA Vector DB](https://help.sap.com/docs/hana-cloud-database/sap-hana-cloud-sap-hana-database-vector-engine-guide/sap-hana-cloud-sap-hana-database-vector-engine-guide?locale=en-US)
- [FAISS](https://github.com/facebookresearch/faiss)
- [PyPDF](https://github.com/py-pdf/pypdf)
- [Streamlit](https://streamlit.io/)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
