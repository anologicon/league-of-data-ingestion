provider "aws" {
    profile = "terraform"
    region = "us-east-1"
}

resource "aws_s3_bucket" "league-data-bronze" {
  bucket = "league-data-bronze"
}

resource "aws_s3_bucket" "league-data-silver" {
  bucket = "league-data-silver"
}

resource "aws_s3_bucket" "league-data-gold" {
  bucket = "league-data-gold"
}

resource "aws_s3_bucket_acl" "league-data-bronze-acl" {
  bucket = aws_s3_bucket.league-data-bronze.id
  acl  = "private"
}

resource "aws_s3_bucket_acl" "league-data-silver-acl" {
  bucket = aws_s3_bucket.league-data-silver.id
  acl  = "private"
}

resource "aws_s3_bucket_acl" "league-data-gold-acl" {
  bucket = aws_s3_bucket.league-data-gold.id
  acl  = "private"
}

resource "aws_s3_bucket_versioning" "league-data-bronze-versioning" {
  bucket = aws_s3_bucket.league-data-bronze.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "league-data-silver-versioning" {
  bucket = aws_s3_bucket.league-data-silver.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "league-data-gold-versioning" {
  bucket = aws_s3_bucket.league-data-gold.id
  versioning_configuration {
    status = "Enabled"
  }
}
