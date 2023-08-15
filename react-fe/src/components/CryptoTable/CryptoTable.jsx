import React from "react";
import CryptoTableHead from "./CryptoTableHead";
import CryptoTableBody from "./CryptoTableBody";
import styles from "./CryptoTable.module.css";

const CryptoTable = ({ data }) => {
  return (
    <div className="table_container">
      <table className={styles.table}>
        <CryptoTableHead />
        <CryptoTableBody data={data} />
      </table>
    </div>
  );
};

export default CryptoTable;
