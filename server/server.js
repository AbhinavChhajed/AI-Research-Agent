const express = require('express');
const cors = require('cors');
const multer = require('multer');
const axios = require("axios");
const formData = require("form-data");
const fs = require("fs");

const upload = multer({ dest: 'uploads/' });

const app = express();
app.use(cors());
app.use(express.json());

const PORT = 5000;

app.post("/analyze",upload.array("files"), async (req, res) => {
    if (!req.files || req.files.length === 0) {
        return res.status(400).json({ error: "No files uploaded." });
    }

    const uploadedFiles = req.files;
    const userPrompt = req.body.userprompt || "";
    const searchEnabled = req.body.searchenabled || "false"; 

    const form = new formData();
    form.append("userprompt", userPrompt);
    form.append("searchenabled", searchEnabled);
    uploadedFiles.forEach(file => {
        form.append("files", fs.createReadStream(file.path));
    });

    try{
        const response = await axios.post("http://localhost:8000/process",form,{
            headers:{
                ...form.getHeaders()
            }
        });
        res.json(response.data);
    }
    catch(e){
        console.error("Error processing files:", e);
        res.status(500).json({ error: "Error processing files." });
    }
})

app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});