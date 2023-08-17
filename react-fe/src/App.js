import React from "react";
import { useState, useEffect } from "react";
import CryptoTable from "./components/CryptoTable/CryptoTable";

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    function getData() {
      fetch("/api/getdata")
        .then((res) => res.json())
        .then((data) => {
          setData(data);
          console.log(data);
        });
    }
    getData();

    const interval = setInterval(() => getData(), 264000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return <>{data && <CryptoTable data={data.data} />}</>;
};

export default App;
