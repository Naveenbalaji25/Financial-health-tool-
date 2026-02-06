import React, { useState } from "react";
import axios from "axios";

function App() {
  const [data, setData] = useState(null);
  const [advice, setAdvice] = useState("");

  const uploadFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file); // key must match 'file' in Flask

    try {
      const res = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setData(res.data);

      const rec = await axios.post("http://127.0.0.1:5000/recommend", {
        score: res.data.score,
      });
      setAdvice(rec.data.advice);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Financial Health Assessment Tool</h1>
      <input type="file" onChange={uploadFile} />

      {data && (
        <div>
          <h2>Results</h2>
          <p>Revenue: {data.revenue}</p>
          <p>Expenses: {data.expenses}</p>
          <p>Profit: {data.profit}</p>
          <p>Health Score: {data.score}</p>

          <h2>AI Advice</h2>
          <p>{advice}</p>
        </div>
      )}
    </div>
  );
}

export default App;