using System;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace RoslynLoad
{

    public static class Encrypt
    {
        //Decrypt
        public static string DecryptString(string cipherText, string key)
        {
            byte[] bytes = Decrypt(Convert.FromBase64String(cipherText), key);
            var utf8 = Encoding.UTF8.GetString(bytes);
            return utf8;
        }

        private static byte[] Decrypt(byte[] bytes, string key)
        {
            byte[] iv = new byte[16]; // change
            Array.Copy(bytes, iv, 16); // change
            AesManaged algorithm = new AesManaged();
            algorithm.IV = iv; // change

            algorithm.Key = Encoding.UTF8.GetBytes(key);

            byte[] ret = null;
            using (var decryptor = algorithm.CreateDecryptor())
            {
                using (MemoryStream msDecrypted = new MemoryStream())
                {
                    using (CryptoStream csEncrypt = new CryptoStream(msDecrypted, decryptor, CryptoStreamMode.Write))
                    {
                        csEncrypt.Write(bytes, 16, bytes.Length - 16); // change
                    }
                    ret = msDecrypted.ToArray();
                }
            }
            return ret;
        }
    }

}
