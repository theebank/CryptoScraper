import React from "react";
import { useState, useEffect } from "react";

const App = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    function getData() {
      fetch("/getdata")
        .then((res) => res.json())
        .then((data) => {
          setData(data.datalist);
          console.log(data);
        });
    }
    getData();

    const interval = setInterval(() => getData(), 60000);
    return () => {
      clearInterval(interval);
    };
  }, []);

  return (
    <>
      {data &&
        data.map((i, key) => (
          <div key={key}>
            <h1>{i.name}</h1>
            <h2>{i.price}</h2>
          </div>
        ))}
    </>
  );
};

export default App;
