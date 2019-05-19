<?php
class Connection {
    private $host = "sql304.epizy.com";
    private $db_name = "epiz_23925804_cbioportal";
    private $username = "epiz_23925804";
    private $password = "Ifsjjw8422o9lg9";
    public $conn;
    // get the database connection
    public function getConnection() {   
        $this->conn = null;
        try {
            $this->conn = new PDO("mysql:host=" . $this->host . ";dbname=" . $this->db_name, $this->username, $this->password);
        } catch (PDOException $exception) {
            echo "Connection error: " . $exception->getMessage();
        }
        return $this->conn;
    }
}
?>