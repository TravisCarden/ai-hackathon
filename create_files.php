<?php

$moduleFolderPath = rtrim($argv[1] ?? '', DIRECTORY_SEPARATOR);
$contentsFilePath = $argv[2] ?? '';

if (!is_dir($moduleFolderPath)) {
  echo "Error: The provided module path does not exist or is not a directory.\n";
  exit(1);
}

if (!file_exists($contentsFilePath)) {
  echo "Error: The provided file contents path does not exist.\n";
  exit(1);
}

$jsonContents = file_get_contents($contentsFilePath);
$filesArray = json_decode($jsonContents, true);

if (json_last_error() !== JSON_ERROR_NONE) {
  echo "Error decoding JSON: " . json_last_error_msg();
  exit(1);
}

foreach ($filesArray as $file) {
  $filePath = $moduleFolderPath . DIRECTORY_SEPARATOR . $file['path'];
  $fileContents = $file['contents'];
  $dirName = dirname($filePath);

  if (!file_exists($dirName)) {
    mkdir($dirName, 0777, true);
  }

  file_put_contents($filePath, $fileContents);
}
