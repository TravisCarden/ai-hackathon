<?php

$moduleFolderPath = realpath($argv[1] ?? '');

if (!is_dir($moduleFolderPath)) {
  echo "The provided path does not exist or is not a directory.\n";
  exit(1);
}

$moduleName = basename($moduleFolderPath);
$outputDirectory = __DIR__ . DIRECTORY_SEPARATOR . 'output';
$outputFilePath = $outputDirectory . DIRECTORY_SEPARATOR . $moduleName . '.contents.json';

if (!is_dir($outputDirectory)) {
  mkdir($outputDirectory, 0755, true);
}

$iterator = new RecursiveIteratorIterator(
  new RecursiveDirectoryIterator($moduleFolderPath, RecursiveDirectoryIterator::SKIP_DOTS),
  RecursiveIteratorIterator::SELF_FIRST
);

$fileData = [];
$basePathLength = strlen($moduleFolderPath) + 1;

foreach ($iterator as $item) {
  if ($item->isFile()) {
    $relativePath = substr($item->getPathname(), $basePathLength);
    $fileContents = file_get_contents($item);

    $fileData[] = [
      'path' => $relativePath,
      'contents' => $fileContents
    ];
  }
}

file_put_contents($outputFilePath, json_encode($fileData, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES));
echo "Module contents have been written to: " . $outputFilePath . "\n";
