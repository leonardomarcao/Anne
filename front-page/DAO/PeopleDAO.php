<?php

include_once 'Connection.php';

class PeopleDAO {

    private $db;

    function __construct() {

        $con = new Connection();
        $this->db = $con->getConnection();
    }

    public function search() {
        $sql = "SELECT * FROM tb_people";
        $stmt = $this->db->prepare($sql);

        $stmt->execute();
        $result = $stmt->fetchAll();
        return $result;
    }

    public function findFeatures($id_categoria) {
        $sql = "SELECT * FROM tb_people WHERE id='$id_categoria'";
        $stmt = $this->db->prepare($sql);

        $stmt->execute();
        $result = $stmt->fetchAll();
        return $result;
    }
}
