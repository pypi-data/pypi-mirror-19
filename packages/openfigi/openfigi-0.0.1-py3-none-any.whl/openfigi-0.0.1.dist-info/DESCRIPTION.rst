Copyright (c) 2016 Julian Wergieluk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Description: # openfigi
        
        Simple wrapper and a command-line tool for Bloomberg's OpenFIGI API.
        
        The API specification is located under [https://www.openfigi.com/api].
        
        ## Usage
        
            import openfigi
            openfigi = OpenFigi('abcdefghijklmnopqrstuvwxyz')
            openfigi.enqueue_request(id_type='ID_WERTPAPIER', id_value='XM91CQ', mic_code='EUWX')
            print(openfigi.fetch_responce())
        
        ## Cli usage
        
            $ openfigi.py --help
            Usage: openfigi.py [OPTIONS] ID_TYPE ID_VALUE
            
            Options:
              --exchange_code TEXT  An optional exchange code if it applies(cannot use
                                    with mic_code).
              --mic_code TEXT       An optional ISO market identification code(MIC) if it
                                    applies(cannot use with exchange_code).
              --currency TEXT       An optional currency if it applies.
              --help                Show this message and exit.
        
        Sample call:
        
            $ openfigi.py --mic_code EUWX ID_WERTPAPIER XM91CQ
            [
                {
                    "data": [
                        {
                            "compositeFIGI": "BBG00BP73295",
                            "exchCode": "GW",
                            "figi": "BBG00BP732P7",
                            "marketSector": "Equity",
                            "name": "DEUTSCH-PW17 DAX INDEX",
                            "securityType": "Index WRT",
                            "shareClassFIGI": null,
                            "ticker": "XM91CQ",
                            "uniqueID": "EQ0000000047042754",
                            "uniqueIDFutOpt": null
                        }
                    ]
                }
            ]
        
        The cli tool searches for 'openfigi_key' environment variable and uses it to
        authenticate. If this fails, an anonymous access is used. 
        
Platform: UNKNOWN
Classifier: Development Status :: 4 - Beta
Classifier: License :: OSI Approved :: MIT License
Classifier: Programming Language :: Python :: 3
