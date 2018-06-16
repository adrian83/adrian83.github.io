---
title: "Converting between numeric types in Haskell"
date: 2018-06-05
categories:
- haskell
tags:
- haskell
thumbnailImagePosition: left
thumbnailImage: https://wiki.haskell.org/wikiupload/4/4a/HaskellLogoStyPreview-1.png
---

As a Haskell rookie I was often surprised that doing things like `sqrt intValue` just won't compile.
<!--more-->


### Short introduction to Haskell numeric types
1. Int - fixed-width machine-specific integers
2. Integer - arbitrary-precision integers
3. Float - single-precision floating-point number
4. Double - double-precision floating-point number
5. Rational - arbitrary-precision fractions

### Types
1. Num contains Int, Integer, Float, Double and Rational
2. Integral contains Int and Integer
3. RealFrac contains Float, Double and Rational
4. Real contains Integral and RealFrac types




Below you can find examples of conversion between few basic Haskell numeric types (Int, Integer, Float, Double, Rational) and String.


## From Int to...

{{< codeblock "from_int.hs" "haskell" "https://github.com/adrian83/playground-haskell/blob/master/conversion/from_int.hs" "from_int.hs" >}}

intToInteger :: Int -> Integer
intToInteger i = toInteger i

intToFloat :: Int -> Float
intToFloat i = fromIntegral i

intToDouble :: Int -> Double
intToDouble i = fromIntegral i

intToRational :: Int -> Rational
intToRational i = fromIntegral i

intToString :: Int -> String
intToString i = show i


main :: IO ()
main = do
    print $ intToInteger 3
    print $ intToFloat 2
    print $ intToDouble 2
    print $ intToRational 7
    print $ intToString 9
{{< /codeblock >}}

{{< codeblock "output" "txt" >}}

$ runhaskell from_int.hs
3
2.0
2.0
7 % 1
"9"

{{< /codeblock >}}



## From Integer to...

{{< codeblock "from_integer.hs" "haskell" "https://github.com/adrian83/playground-haskell/blob/master/conversion/from_integer.hs" "from_integer.hs" >}}

integerToInt :: Integer -> Int
integerToInt i = fromIntegral i

integerToFloat :: Integer -> Float
integerToFloat i = fromInteger i

integerToDouble :: Integer -> Double
integerToDouble i = fromInteger i

integerToRational :: Integer -> Rational
integerToRational i = fromInteger i

integerToString :: Integer -> String
integerToString i = show i


main :: IO ()
main = do
    print $ integerToInt 8
    print $ integerToFloat 6
    print $ integerToDouble 2
    print $ integerToRational 7
    print $ integerToString 9
{{< /codeblock >}}

{{< codeblock "output" "txt" >}}

$ runhaskell from_integer.hs
8
6.0
2.0
7 % 1
"9"

{{< /codeblock >}}



## From Float to...

{{< codeblock "from_float.hs" "haskell" "https://github.com/adrian83/playground-haskell/blob/master/conversion/from_float.hs" "from_float.hs" >}}

import GHC.Float

floatToIntRound :: Float -> Int
floatToIntRound f = round f

floatToIntCeiling :: Float -> Int
floatToIntCeiling f = ceiling f

floatToIntFloor :: Float -> Int
floatToIntFloor f = floor f

floatToIntegerRound :: Float -> Integer
floatToIntegerRound f = round f

floatToIntegerCeiling :: Float -> Integer
floatToIntegerCeiling f = ceiling f

floatToIntegerFloor :: Float -> Integer
floatToIntegerFloor f = floor f

floatToDouble :: Float -> Double
floatToDouble f = float2Double f

floatToRational :: Float -> Rational
floatToRational f = toRational f

floatToString :: Float -> String
floatToString f = show f


main :: IO ()
main = do
    print $ floatToIntRound 1.3
    print $ floatToIntCeiling 1.1
    print $ floatToIntFloor 1.8
    print $ floatToIntegerRound 1.3
    print $ floatToIntegerCeiling 1.1
    print $ floatToIntegerFloor 1.8
    print $ floatToDouble 1.2
    print $ floatToRational 1.22
    print $ floatToString 4.3
{{< /codeblock >}}

{{< codeblock "output" "txt" >}}

$ runhaskell from_float.hs
1
2
1
1
2
1
1.2000000476837158
5117051 % 4194304
"4.3"

{{< /codeblock >}}



## From Double to...

{{< codeblock "from_double.hs" "haskell" "https://github.com/adrian83/playground-haskell/blob/master/conversion/from_double.hs" "from_double.hs" >}}

doubleToIntRound :: Double -> Int
doubleToIntRound f = round f

doubleToIntCeiling :: Double -> Int
doubleToIntCeiling f = ceiling f

doubleToIntFloor :: Double -> Int
doubleToIntFloor f = floor f

doubleToIntegerRound :: Double -> Integer
doubleToIntegerRound f = round f

doubleToIntegerCeiling :: Double -> Integer
doubleToIntegerCeiling f = ceiling f

doubleToIntegerFloor :: Double -> Integer
doubleToIntegerFloor f = floor f

doubleToFloat :: Double -> Float
doubleToFloat f = realToFrac f

doubleToRational :: Double -> Rational
doubleToRational f = toRational f

doubleToString :: Double -> String
doubleToString f = show f


main :: IO ()
main = do
    print $ doubleToIntRound 1.3
    print $ doubleToIntCeiling 1.1
    print $ doubleToIntFloor 1.8
    print $ doubleToIntegerRound 1.3
    print $ doubleToIntegerCeiling 1.1
    print $ doubleToIntegerFloor 1.8
    print $ doubleToFloat 1.2
    print $ doubleToRational 1.22
    print $ doubleToString 4.3
{{< /codeblock >}}

{{< codeblock "output" "txt" >}}

$ runhaskell from_double.hs
1
2
1
1
2
1
1.2
5494391545392005 % 4503599627370496
"4.3"

{{< /codeblock >}}



## From Rational to...

{{< codeblock "from_rational.hs" "haskell" "https://github.com/adrian83/playground-haskell/blob/master/conversion/from_rational.hs" "from_rational.hs" >}}

import Data.Ratio

rationalToString :: Rational -> String
rationalToString r = show r

rationalToIntRound :: Rational -> Int
rationalToIntRound r = round (fromRational r)

rationalToIntCeiling :: Rational -> Int
rationalToIntCeiling r = ceiling (fromRational r)

rationalToIntFloor :: Rational -> Int
rationalToIntFloor r = floor (fromRational r)

rationalToIntegerRound :: Rational -> Integer
rationalToIntegerRound r = round (fromRational r)

rationalToIntegerCeiling :: Rational -> Integer
rationalToIntegerCeiling r = ceiling (fromRational r)

rationalToIntegerFloor :: Rational -> Integer
rationalToIntegerFloor r = floor (fromRational r)

rationalToFloat :: Rational -> Float
rationalToFloat r = fromRational r

rationalToDouble :: Rational -> Double
rationalToDouble r = fromRational r

main :: IO ()
main = do
    print $ rationalToString (2 % 3)
    print $ rationalToIntRound (2 % 3)
    print $ rationalToIntCeiling (2 % 3)
    print $ rationalToIntFloor (2 % 3)
    print $ rationalToIntegerRound (2 % 3)
    print $ rationalToIntegerCeiling (2 % 3)
    print $ rationalToIntegerFloor (2 % 3)
    print $ rationalToFloat (2 % 3)
    print $ rationalToDouble (2 % 3)
{{< /codeblock >}}

{{< codeblock "output" "txt" >}}

$ runhaskell from_rational.hs
"2 % 3"
1
1
0
1
1
0
0.6666667
0.6666666666666666

{{< /codeblock >}}




## From String to...

{{< codeblock "from_string.hs" "haskell" "https://github.com/adrian83/playground-haskell/blob/master/conversion/from_string.hs" "from_string.hs" >}}

stringToInt :: String -> Int
stringToInt s = read s :: Int

stringToInteger :: String -> Integer
stringToInteger s = read s :: Integer

stringToFloat :: String -> Float
stringToFloat s = read s :: Float

stringToDouble :: String -> Double
stringToDouble s = read s :: Double

stringToRational:: String -> Rational
stringToRational s = toRational ( read s :: Float )


main :: IO ()
main = do
    print $ stringToInt "3"
    print $ stringToInteger "2"
    print $ stringToFloat "4.2"
    print $ stringToDouble "1.32"
    print $ stringToRational "1.3"
{{< /codeblock >}}

{{< codeblock "output" "txt" >}}

$ runhaskell from_string.hs
3
2
4.2
1.32
5452595 % 4194304

{{< /codeblock >}}
