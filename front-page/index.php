
<!DOCTYPE html>
<html lang="en">

<head>

  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>Mqtt</title>

  <!-- Bootstrap core CSS -->
  <link href="vendor/bootstrap/css/bootstrap.min.css" rel="stylesheet">

  <!-- Custom fonts for this template -->
  <link href="https://fonts.googleapis.com/css?family=Saira+Extra+Condensed:500,700" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Muli:400,400i,800,800i" rel="stylesheet">
  <link href="vendor/fontawesome-free/css/all.min.css" rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="css/resume.min.css" rel="stylesheet">

</head>

<body id="page-top">
<?php
    include_once './DAO/PeopleDAO.php';
     $dao = new PeopleDAO();
     $people = $dao->findFeatures($_GET['id'])
     
?>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top" id="sideNav">
    <a class="navbar-brand js-scroll-trigger" href="#page-top">
      <?php if($_GET['id'] > 0){ ?>
      <span class="d-block d-lg-none">Bem Vindo</span>
      <span class="d-block d-lg-none">
        <?php echo $people[0][1]; ?></span>
      <?php }else{ ?>
        <h1 class="mb-0">
            <span class="text-primary">Acesso Negado</span>
          </h1>
      <?php } ?>
      <span class="d-none d-lg-block">
        <img class="img-fluid img-profile rounded-circle mx-auto mb-2" src="img/profile.jpg" alt="">
      </span>
        <img class="img-fluid img-profile rounded-circle mx-auto mb-2" src="<?php echo "img/".$people[0][0].".jpg"; ?>" alt="">
    </a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
  
  </nav>

  <div class="container-fluid p-0">

    <section class="resume-section p-3 p-lg-5 d-flex align-items-center" id="about">
      
    <?php if($_GET['id'] > 0){ ?>
      <div class="w-100">
        <h1 class="mb-0">
          <span class="text-primary">Bem vindo</span>
        </h1>
        <h1 class="mb-0">
          <?php echo $people[0][1]; ?>
        </h1>
       </div>
      <?php }else{ ?>
      <h1 class="mb-0">
          <span class="text-primary">Acesso Negado</span>
        </h1>
      <?php } ?>
      
    </section>

    <hr class="m-0">

  
    <hr class="m-0">

    <hr class="m-0">

    <hr class="m-0">

    <hr class="m-0">

  </div>

  <!-- Bootstrap core JavaScript -->
  <script src="vendor/jquery/jquery.min.js"></script>
  <script src="vendor/bootstrap/js/bootstrap.bundle.min.js"></script>

  <!-- Plugin JavaScript -->
  <script src="vendor/jquery-easing/jquery.easing.min.js"></script>

  <!-- Custom scripts for this template -->
  <script src="js/resume.min.js"></script>

</body>

</html>


