import React from "react";

const CryptoTableBody = ({ data }) => {
  return (
    <tbody>
      {data &&
        data.map((i, key) => {
          return (
            <tr key={key}>
              <td>{key + 1}</td>
              <td>{i.name}</td>
              <td>{i.price}</td>
            </tr>
          );
        })}
    </tbody>
  );
};

export default CryptoTableBody;
