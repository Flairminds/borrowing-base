import { Modal } from "antd";
import React from "react";

export const CellDetailsModal = ({ visible, onClose, cellDetails }) => {
  return (
    <Modal
      title="Cell Details"
      open={visible}
      onCancel={onClose}
      footer={null}
    >
      <p>
        <strong>Row Index:</strong> {cellDetails?.rowIndex ?? "-"}
      </p>
      <p>
        <strong>Column:</strong> {cellDetails?.column ?? "-"}
      </p>
      <p>
        <strong>Value:</strong> {cellDetails?.cellValue ?? "-"}
      </p>
    </Modal>
  );
};

