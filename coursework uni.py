import numpy as np
# Caesar Cipher
cipherAlphabets = {
    'default' : 'abcdefghijklmnopqrstuvwxyz',
    'vowels' : 'aeiou',
    'consonants' : 'bcdfghjklmnpqrstvwxyz',
    'qwerty' : 'qwertyuiopasdfghjklzxcvbnm',
    'ambidextrous' : 'ambidextrous'
}
class IdentityCipher(object):
    '''Returns identity cipher'''
    def __init__(self,alphabet='default'):
        if alphabet in cipherAlphabets:
            self.alphabet = cipherAlphabets[alphabet]
        else:
            self.alphabet = alphabet
    def encode(self,message):
        return message
    def decode(self,message):
        return message
    def __compose__(self,second):
        return second
    def __pow__(self,exponent):
        return self
    def demonstrate(self,messages,title="Identity Cipher"):
        print("\n"+"="*80)
        print(title)
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
class CipherComposition(object):
    '''Composes any cipher'''
    def __init__(self,ciphers):
        self.ciphers = ciphers
    def encode(self,message):
        result = message
        for i in self.ciphers:
            result = i.encode(result)
        return result
    def decode(self,message):
        result = message
        for i in reversed(self.ciphers):
            result = i.decode(result)
        return result
    def __compose__(self,second):
        '''Applies second then self'''
        return CipherComposition([second]+self.ciphers)
    def __pow__(self,exponent):
        '''Applies entire composition exponent times'''
        if not isinstance(exponent,int) or exponent < 0:
            raise Exception(f"Exponent must be non-negative int, not {exponent}")
        if exponent == 0:
            if not self.ciphers:
                return IdentityCipher('default')
            return IdentityCipher(self.ciphers[0].alphabet if self.ciphers else 'default')
        result = []
        for i in range(exponent):
            result.extend(self.ciphers)
        return CipherComposition(result)
    def demonstrate(self,messages,title="Cipher Composition"):
        print("\n"+"="*80)
        print(title)
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
class CaesarCipher(object):
    ''' Caesar Cipher with any chosen shift'''
    def __init__(self,shift,alphabet = 'default'):
        # Validating input
        if alphabet in cipherAlphabets:
            alphabetStr = cipherAlphabets[alphabet]
        else:
            alphabetStr = alphabet
        if not isinstance(shift,int):
            raise Exception(f"Shift should be int, not {type(shift)}.")
        if len(set(alphabetStr)) != len(alphabetStr):
            raise Exception("Alphabet must include distinct characters")
        self.shift = shift
        self.alphabet = alphabetStr
        n = len(alphabetStr)
        self.encodedAlphabet = {}
        self.decodedAlphabet = {}
        for i in range(n):
            character = alphabetStr[i]
            self.encodedAlphabet[character] = alphabetStr[(i+shift)%n]
            self.decodedAlphabet[character] = alphabetStr[(i-shift)%n]
    def CaseCheck(self, message, mapping):
        result = []
        for numChar in message:
            lowerChar = numChar.lower()
            if lowerChar in mapping:
                mapped = mapping[lowerChar]
                if numChar.isupper():
                    result.append(mapped.upper())
                else:
                    result.append(mapped)
            else:
                result.append(numChar)
        return ''.join(result)
    def encode(self,plaintext): 
        return self.CaseCheck(plaintext,self.encodedAlphabet)
    def decode(self,ciphertext): 
        return self.CaseCheck(ciphertext,self.decodedAlphabet)
    def demonstrate(self,messages):
        print("\n"+"="*80)
        print(f"Caesar Cipher C_{self.shift} (shift = {self.shift})")
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
    # Operator Overloading for part B
    def __compose__(self,second):
        if self.alphabet == second.alphabet:
            return CaesarCipher(self.shift + second.shift,self.alphabet)
        else:
            return CipherComposition([second,self])
    def __add__(self,second):
        '''Addition where C_c1+C_c2 = C_{c1+c2}, same alphabet required.'''
        if self.alphabet != second.alphabet:
            raise Exception(f"Cannot add different alphabets")
        return CaesarCipher(self.shift+second.shift,self.alphabet)
    def __mul__(self,scalar):
        '''Scalar multiplication: n*C_C=C_{n*c}'''
        if not isinstance(scalar,int):
            raise Exception(f"Scalar must be int, not {type(scalar)}.")
        return CaesarCipher(scalar*self.shift, self.alphabet)
    def __rmul__(self,scalar):
        '''Allows commutativity for scalar mult'''
        return self.__mul__(scalar)
    def __pow__(self,exponent):
        '''Exponents C_c^n=C_{n*c}'''
        if not isinstance(exponent,int):
            raise Exception(f"Exponent must be int, not {type(exponent)}.")
        return CaesarCipher(exponent*self.shift, self.alphabet)
messages = [
    ('bond','Agent 007: "Shaken, not stirred!"'),
    ('holmes','[At 221B Baker Street] Holmes (to Watson): "Elementary. my dear Watson!"'),
    ('joker','Why so serious?! Let\'s put a smile on that face.'),
    ('turing','In 1950, Turing asked: "Can machines think?"'),
    ('hamlet','[Act 3, Scene 1] To be, or not to be?'),
    ('enigma','[Bletchley, 1941] The Enigma has been cracked!')
]
C_3 = CaesarCipher(3,'default').demonstrate(messages)
C_minus_5 = CaesarCipher(-5,'default').demonstrate(messages)
# Justification:
# I decided to create several classes, notably the CaesarCipher class, in order for the code to be reusable, allowing easy use for several ciphers with varying shifts and alphabets. Within this class, instead of needing to recompute the shifted index for every character during the encoding and decoding phases, the required shifting is all within init, allowing increased efficiency for any message. I used the set() function to ensure any alphabet used includes only distinct characters for an unambiguous decoding. I also defined a function CaseCheck to preserve case, whilst also applying a given mapping, in this case one of the alphabet dictionaries, to every character in the message. Error handling is also present here, as I have included checks for if the shift is an integer, the alphabet containing distinct characters, and that the alphabet is within the cipherAlphabets dictionary, preventing logical errors. Using the str.join function allows me to build the output string much more efficiently too. To decode some cipher C_c, we notice the alphabet has been shifted forward by c, so decoding requires us to shift the encoded message back by c. Within my code, self.decodedAlphabet[character] = alphabetStr[(i-shift)%n] allows me to decode some message, where i is is the index of the character, and n is the length of the alphabet. For example, say we encoded 'b' within C_3, using the default alphabet. This is index 1 here, so to encode we shift it forward 3 positions: (1+3)%26=4=e. So 'b' gives us 'e'. Decoding: 'e' gives us (4-3)%26=1 which is 'b' here. This applies for any shift and any alphabet.

# Affine Cipher
cipherAlphabets = {
    'default' : 'abcdefghijklmnopqrstuvwxyz',
    'vowels' : 'aeiou',
    'consonants' : 'bcdfghjklmnpqrstvwxyz',
    'qwerty' : 'qwertyuiopasdfghjklzxcvbnm',
    'ambidextrous' : 'ambidextrous'
}
class CipherComposition(object):
    '''Composes any cipher'''
    def __init__(self,ciphers):
        self.ciphers = ciphers
    def encode(self,message):
        result = message
        for i in self.ciphers:
            result = i.encode(result)
        return result
    def decode(self,message):
        result = message
        for i in reversed(self.ciphers):
            result = i.decode(result)
        return result
    def __compose__(self,second):
        '''Applies second then self'''
        return CipherComposition([second]+self.ciphers)
    def __pow__(self,exponent):
        '''Applies entire composition exponent times'''
        if not isinstance(exponent,int) or exponent < 0:
            raise Exception(f"Exponent must be non-negative int, not {exponent}")
        if exponent == 0:
            if not self.ciphers:
                return IdentityCipher('default')
            return IdentityCipher(self.ciphers[0].alphabet if self.ciphers else 'default')
        result = []
        for i in range(exponent):
            result.extend(self.ciphers)
        return CipherComposition(result)
    def demonstrate(self,messages,title="Cipher Composition"):
        print("\n"+"="*80)
        print(title)
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
class AffineCipher(object):
    ''' Affine Cipher with any chosen scalar multiple a, and shift b'''
    def __init__(self,scalar,shift,alphabet = 'default'):
        # Validating input
        if alphabet in cipherAlphabets:
            alphabetStr = cipherAlphabets[alphabet]
        else:
            alphabetStr = alphabet
        if not isinstance(shift,int):
            raise Exception(f"Shift should be int, not {type(shift)}.")
        if not isinstance(scalar,int) or not isinstance(shift,int):
            raise Exception(f"a and b must be integers, not a={type(scalar)}, b={type(shift)}")
        if len(set(alphabetStr)) != len(alphabetStr):
            raise Exception("Alphabet must include distinct characters")
        self.shift = shift
        self.scalar = scalar
        self.alphabet = alphabetStr
        n = len(alphabetStr)
        self.encodedAlphabet = {}
        self.decodedAlphabet = {}
        # Modular inverse of a mod n
        self.inverse = None
        for i in range(n):
            if (scalar*i) % n == 1:
                self.inverse = i
                break
        if self.inverse is None:
            raise Exception(f"{scalar} has no inverse modulo {n}.")
        for i in range(n):
            character = alphabetStr[i]
            self.encodedAlphabet[character] = alphabetStr[(scalar*i+shift)%n]
            self.decodedAlphabet[character] = alphabetStr[(self.inverse*(i-shift))%n]
    def CaseCheck(self, message, mapping):
        result = []
        for numChar in message:
            lowerChar = numChar.lower()
            if lowerChar in mapping:
                mapped = mapping[lowerChar]
                if numChar.isupper():
                    result.append(mapped.upper())
                else:
                    result.append(mapped)
            else:
                result.append(numChar)
        return ''.join(result)
    def encode(self,plaintext): 
        return self.CaseCheck(plaintext,self.encodedAlphabet)
    def decode(self,ciphertext): 
        return self.CaseCheck(ciphertext,self.decodedAlphabet)
    def demonstrate(self,messages):
        print("\n"+"="*80)
        print(f"Affine Cipher A_({self.scalar},{self.shift}) (a = {self.scalar}, b = {self.shift})")
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
        return self
    # Operator overloading for part B
    def __compose__(self,second):
        if self.alphabet == second.alphabet and self.scalar == second.scalar:
            return AffineCipher(self.scalar, self.shift+second.shift,self.alphabet)
        else:
            return CipherComposition([second,self])
    def __add__(self,second):
        '''Addition where A_c1+C_c2 = C_{c1+c2}, same alphabet required.'''
        if self.alphabet != second.alphabet:
            raise Exception(f"Cannot add different alphabets")
        elif self.scalar != second.scalar:
            raise Exception(f"Cannot add with different multipliers")
        return AffineCipher(self.scalar,self.shift+second.shift,self.alphabet)
    def __mul__(self,scalar):
        '''Scalar multiplication: n*A_{a,b}=A_{a,n*b}'''
        if not isinstance(scalar,int):
            raise Exception(f"Scalar must be int, not {type(scalar)}.")
        return AffineCipher(self.scalar,scalar*self.shift, self.alphabet)
    def __rmul__(self,scalar):
        '''Allows commutativity for scalar mult'''
        return self.__mul__(scalar)
    def __pow__(self,exponent):
        '''Exponents A_{a,b}^n=A_{a,n*b}'''
        if not isinstance(exponent,int):
            raise Exception(f"Exponent must be int, not {type(exponent)}.")
        return AffineCipher(self.scalar,exponent*self.shift, self.alphabet)
messages = [
    ('bond','Agent 007: "Shaken, not stirred!"'),
    ('holmes','[At 221B Baker Street] Holmes (to Watson): "Elementary. my dear Watson!"'),
    ('joker','Why so serious?! Let\'s put a smile on that face.'),
    ('turing','In 1950, Turing asked: "Can machines think?"'),
    ('hamlet','[Act 3, Scene 1] To be, or not to be?'),
    ('enigma','[Bletchley, 1941] The Enigma has been cracked!')
]
A_7_3 = AffineCipher(7,3,'default').demonstrate(messages)
A_5_8 = AffineCipher(5,8,'default').demonstrate(messages)
# Justification
# The Affine cipher is very similar to the Caesar Cipher, and can be shown within my code: the idea of encoding is practically the same, except we multiply i, which is the index of the character within a message, by some scalar 'a' defined in the init here. This was done for consistency across these ciphers. Since we have that scalar multiplier for i, we need a modular inverse for a, hence I created a loop allowing self.inverse to be a^{-1}. It is efficient for the size of the alphabets given. I also would raise an exception if no inverse is possible, preventing indecipherable code. CaseCheck is still relevant here, from A1, accepting a mapping dictionary and applying it to every character, preserving case. To decode some given cipher A_{a,b}, consider encoding some text m: w = (a*m+b) mod n, where w is our encoded message, and n is the size of the alphabet. Solving for m we get w = a^{-1}x(y-b) mod n, where a^{-1} is the modular inverse of a mod n. This exists if and only if gcd(a,n) = 1. b can be an integer, but less restriction there. For example, let's use A_{7,3} with the default alphabet, where n = 26 First note gcd(7,26)=1, so there is an inverse, 15. Encode 'b' (index 1): (7x1+3) mod 26 = 10 which is 'k' Decode 'k' (index 10): 15x(10-3) mod 26 = 1 which is 'b'! For an invalid example, use A_{2,0} Notice gcd(2,26)=2, so there should be no inverse. Encode 'a' (index 0): 2x0 mod 26 = 0 which is 'a' But encode 'n' (index 13) we get 13x2 = 26 mod 26 = 0 which is also 'a', so the decoding is ambiguous. My code will raise an exception.

# Substitution Cipher
class SubstitutionCipher(object):
    ''' Substitution Cipher with a reverse and split permutation'''
    def __init__(self,permutation,alphabet='default'):
        # Validating input
        if alphabet in cipherAlphabets:
            alphabetStr = cipherAlphabets[alphabet]
        else:
            alphabetStr = alphabet
        if len(set(alphabetStr)) != len(alphabetStr):
            raise Exception("Alphabet must include distinct characters")
        self.alphabet = alphabetStr
        n = len(alphabetStr)
        left=[]
        right=[]
        self.permutation = permutation
        if permutation == 'reverse':
            permuteStr = alphabetStr[::-1]
        elif permutation == 'split':
            for i in range(n):
                if i%2 == 0:
                    left.append(alphabetStr[i])
                else:
                    right.append(alphabetStr[i])
            permuteStr = ''.join(left+right[::-1])
        else:
            permuteStr = permutation
        if len(permuteStr) != n:
            raise Exception(f"Length of permutation = {len(permuteStr)} does not match alphabet length {n}.")

        self.encodedAlphabet = {}
        self.decodedAlphabet = {}
        for i in range(n):
            originalCharacter = alphabetStr[i]
            permuteCharacter = permuteStr[i]
            self.encodedAlphabet[originalCharacter] = permuteCharacter
            self.decodedAlphabet[permuteCharacter] = originalCharacter
    def CaseCheck(self, message, mapping):
        result = []
        for numChar in message:
            lowerChar = numChar.lower()
            if lowerChar in mapping:
                mapped = mapping[lowerChar]
                if numChar.isupper():
                    result.append(mapped.upper())
                else:
                    result.append(mapped)
            else:
                result.append(numChar)
        return ''.join(result)
    def encode(self,plaintext): 
        return self.CaseCheck(plaintext,self.encodedAlphabet)
    def decode(self,ciphertext): 
        return self.CaseCheck(ciphertext,self.decodedAlphabet)
    def demonstrate(self,messages):
        print("\n"+"="*80)
        print(f"Substitution Cipher S_({self.permutation}) (permutation = {self.permutation})")
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
    # Operator overloading for part B
    def __compose__(self,second):
        composedAlphabet = []
        # Applies second first, then self
        for characters in self.alphabet:
            stepOne = second.encode(characters)
            stepTwo = self.encode(stepOne)
            composedAlphabet.append(stepTwo)
        composedPerm = ''.join(composedAlphabet)
        return SubstitutionCipher(composedPerm,self.alphabet)
    def __pow__(self,exponent):
        if not isinstance(exponent,int) or exponent < 0:
            raise Exception(f"Exponent must be non-negative int, not {exponent}")
        elif exponent == 0:
            return SubstitutionCipher(self.alphabet,self.alphabet)
        result = self
        for i in range(exponent-1):
            result = result.__compose__(self)
        return result
messages = [
    ('bond','Agent 007: "Shaken, not stirred!"'),
    ('holmes','[At 221B Baker Street] Holmes (to Watson): "Elementary. my dear Watson!"'),
    ('joker','Why so serious?! Let\'s put a smile on that face.'),
    ('turing','In 1950, Turing asked: "Can machines think?"'),
    ('hamlet','[Act 3, Scene 1] To be, or not to be?'),
    ('enigma','[Bletchley, 1941] The Enigma has been cracked!')
]
S_reverse = SubstitutionCipher('reverse','default').demonstrate(messages)
S_split = SubstitutionCipher('split','default').demonstrate(messages)
# Justification
# The cipher is defined by a permutation, where the implementation accepts a named one, namely 'reverse' or 'split', or a custom one of the same length as the alphabet, allowing flexibilty. For each index i in the alphabet, the original character alphabetStr[i] is mapped to its permuteStr[i]. The decoding simply stores the reverse mapping, which allows for efficient encoding and decoding. CaseCheck is also relevant here. To decode some cipher S_p, we use the inverse permutation p^{-1}. In my code, the decoding dictionary is built directly via mapping the inverse via CaseCheck: self.decodedAlphabet[permuteCharacter] = originalCharacter Let's use S_{reverse} The permutation maps 'abcdefghijklmnopqrstuvwxyz' to 'zyxwvutsrqponmlkjihgfedcba', so encoding 'a' goes to 'z', and using the decoding dictionary we see 'z' goes to 'a'. Since the permutation is always bijective from my error handling, decoding always recovers the original message uniquely.

# Custom Alphabet
messages = [
    ('bond','Agent 007: "Shaken, not stirred!"'),
    ('holmes','[At 221B Baker Street] Holmes (to Watson): "Elementary. my dear Watson!"'),
    ('joker','Why so serious?! Let\'s put a smile on that face.'),
    ('turing','In 1950, Turing asked: "Can machines think?"'),
    ('hamlet','[Act 3, Scene 1] To be, or not to be?'),
    ('enigma','[Bletchley, 1941] The Enigma has been cracked!')
]
C_3 = CaesarCipher(3,'vowels').demonstrate(messages)
A_2_5_consonants = AffineCipher(2,5,'consonants').demonstrate(messages)
S_reverse = SubstitutionCipher('reverse','qwerty').demonstrate(messages)
S_split = SubstitutionCipher('split','ambidextrous').demonstrate(messages)
# Justification
# I created a dictonary cipherAlphabets to store alphabets such as 'default', 'vowels' etc., allowing ciphers to be used with a name instead of reusing the long string of characters. Within each class I created an alphabet parameter, allowing not only to select dictionary items, but also custom ones too. This is shown at the top of the init function. Using len(set(alphabetStr))==len(alphabetStr), as said in A1, ensures the mapping is bijective so there is no ambiguous decoding. Since each encoding/decoding operation is implemented used indices relative to the provided alphabet, e.g. len(alphabetStr), I can use any alphabet length and any ordering of characters on my messages.

# Operations on Caesar Cipher
# 1
composed1 = CaesarCipher(3,'vowels').__compose__(CaesarCipher(-5,'vowels')).demonstrate(messages)
# 2
exponent2 = CaesarCipher(3,'ambidextrous') ** 4
exponent2.demonstrate(messages)
# 3
mult3 = 5*CaesarCipher(2)
mult3.demonstrate(messages)
# 4
mult4 = (-1)*CaesarCipher(2,'vowels')
mult4.demonstrate(messages)
# 5
add5 = CaesarCipher(4,'qwerty') + CaesarCipher(3,'qwerty')
add5.demonstrate(messages)
# 6
composed6 = CaesarCipher(3,'vowels').__compose__(CaesarCipher(5,'consonants')).demonstrate(messages)
# Justification
# To support these operations, in A1 I implemented operator overloading within the CaesarCipher class: add allows for cipher addition checking if both of the ciphers' alphabets are the same, raising an exception if not, mul/rmul allows for (commutative) scalar multiplication, pow for exponentiation on non-negative integer n, which is equivalent to scalar multiplication in this context. Operations requiring the same alphabet, such as add compares both alphabets of the ciphers. If they are different, an exception is raised. For composition, firslty, my code checks if the alphabets are the same, returning the addition of the two ciphers if so. If not, I created a new class in A1, CipherComposition, used for both Caesar and Affine, storing both ciphers in order, applying them sequentially. Within this class is further operation overloading, such as encode, decode etc. allowing further composition/operations.

# Operations on Affine Cipher
# 1
composed1 = AffineCipher(5,3,'qwerty').__compose__(AffineCipher(7,2,'qwerty')).demonstrate(messages)
# 2
exponent2 = AffineCipher(5,2,'ambidextrous')**4
exponent2.demonstrate(messages)
# 3
mult3 = 5*AffineCipher(3,2)
mult3.demonstrate(messages)
# 4
mult4 = (-1)*AffineCipher(3,2)
mult4.demonstrate(messages)
# 5
add5 = AffineCipher(4,2,'vowels') + AffineCipher(4,1,'vowels')
add5.demonstrate(messages)
# 6
composed6 = AffineCipher(5,3,'qwerty').__compose__(AffineCipher(8,2,'consonants')).demonstrate(messages)
# Justification
# Like the CaesarCipher, operator overloading is present: add defined only for the same scalar multiple and alphabet, raising an exception if not, returning the sum of the shifts for each cipher. mul/rmul allows for commutative scalar multiplication, returning the same scalar, with a multiple of the shift. Also handles negation. pow for non-negative n. For n=0, identity cipher is returned. compose is practically the same as B1, using CipherComposition. As said in A2, 'a' is only valid when gcd(a,n)=1, where n is the alphabet size.

# Compositions on Substitution Cipher
# 1
S_reverse = SubstitutionCipher('reverse')
S_split = SubstitutionCipher('split')
composition1=S_reverse.__compose__(S_split)
composition1.demonstrate(messages)
# 2
composition2=SubstitutionCipher('reverse','qwerty').__compose__(SubstitutionCipher('split','vowels'))
composition2.demonstrate(messages)
# 3 
exponent3 = SubstitutionCipher('split','ambidextrous')**3
exponent3.demonstrate(messages)
# Justification
# Unlike Caesar and Affine, compose simply iterates over every character in the alphabet, applying the second encoding, then first one, collecting resulting characters. They are then joined together, representing the composed mapping. pow is defined by repeatedly composing the cipher with itself, where for exponent == 0, it returns the identity cipher, then for exponent > 0, it starts with itself, then composes with itself (exponent-1) times using a for loop. To calculate (S_{reverse}^2, we calculate S{reverse}, (e.g. 'a' maps to 'z'). Squaring it means applying the same permutation again, so reversing the reversed string, or getting back to our original message ('z' maps to 'a'). This simply returns our identity cipher.

# Mixed Combination
Cipher = CaesarCipher(2)+4*CaesarCipher(3) + (-2)*CaesarCipher(4)
Sub = SubstitutionCipher('split','vowels') ** 2
Affine = (10 * AffineCipher(5,4,'ambidextrous')).__compose__(AffineCipher(8,2,'consonants'))
Output = ((Cipher.__compose__(Sub))**2).__compose__(Affine)
Output.demonstrate(messages)
# Justification
# For the Caesar ciphers, a,b,c are chosen arbitrarily, since they all share the same alphabet, meaning any values work here. I chose 'default', again randomly, as long as they are the same. For the affine cipher, a_1 is chosen to be 5, with beta being ambidextrous (size 12). This is valid since gcd(5,12)=1, so there is an inverse. Similar for a_2 and gamma (consonants, size 21), since gcd(8,21)=1 as well. b_1 and b_2 are chosen at random. In the Substitution cipher, since the split permutation is always bijective, alpha is chosen randomly too. For the handling, the CaesarCipher part computes, with add and mul, the net shift (6 in this example) to return a single instance. Since the Caesar cipher and Sub cipher use different alphabets, it returns a CipherComposition, storing [SubstitutionCipher,CaesarCipher], applying the sub cipher (which is squared using the pow operator) first. CipherComposition.pow also works, simply composing this new cipher with itself. The affine part also returns a CipherComposition, since they both have different alphabet. The final output simply applies all ciphers in order. The CipherComposition class, as said above applies each stored cipher in order, then decode applies them in reverse, so each expression is evaluated step-by-step. Since each step is also invertible, the overall combination is invertible.

# Affine Hill Cipher
cipherAlphabets = {
    'default' : 'abcdefghijklmnopqrstuvwxyz',
    'vowels' : 'aeiou',
    'consonants' : 'bcdfghjklmnpqrstvwxyz',
    'qwerty' : 'qwertyuiopasdfghjklzxcvbnm',
    'ambidextrous' : 'ambidextrous'
}
messages = [
    ('bond','Agent 007: "Shaken, not stirred!"'),
    ('holmes','[At 221B Baker Street] Holmes (to Watson): "Elementary. my dear Watson!"'),
    ('joker','Why so serious?! Let\'s put a smile on that face.'),
    ('turing','In 1950, Turing asked: "Can machines think?"'),
    ('hamlet','[Act 3, Scene 1] To be, or not to be?'),
    ('enigma','[Bletchley, 1941] The Enigma has been cracked!')
]
class CipherCompositionHill(object):
    '''Composes any Affine Hill cipher'''
    def __init__(self,ciphers):
        if not isinstance(ciphers,list):
            raise Exception(f"Ciphers must be a list")
        if len(ciphers)==0:
            raise Exception(f"Cannot create empty composition")
        self.ciphers = ciphers
    def encode(self,message):
        result = message
        for i in self.ciphers:
            result = i.encode(result)
        return result
    def decode(self,message):
        result = message
        for i in reversed(self.ciphers):
            result = i.decode(result)
        return result
    def __compose__(self,second):
        '''Applies second then self'''
        if not hasattr(second,'encode') or not hasattr(second,'decode'):
            raise Exception(f"Can only comopse with cipher object")
        return CipherCompositionHill([second]+self.ciphers)
    def __pow__(self,exponent):
        '''Applies entire composition exponent times'''
        if not isinstance(exponent,int) or exponent < 0:
            raise Exception(f"Exponent must be non-negative int, not {exponent}")
        if exponent == 0:
            if not self.ciphers:
                return IdentityHill('vowels',2)
                
            return IdentityHill(self.ciphers[0].alphabet,self.ciphers[0].n)
        result = []
        for i in range(exponent):
            result.extend(self.ciphers)
        return CipherCompositionHill(result)
    def demonstrate(self,messages,title="Cipher Composition"):
        print("\n"+"="*80)
        print(title)
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
class AffineHillCipher(object):
    '''Returns affine Hill cipher with block size n, integer (n*n) matrix A, and integer vector b of length n'''
    def __init__(self,A,b,alphabet='vowels'):
        ''' Only required for vowels, but able to change'''
        Amat = np.array(A,dtype=int)
        if Amat.shape[0] != Amat.shape[1]:
            raise Exception(f"Matrix A must be square")
        n = Amat.shape[0]
        Bvec = np.array(b,dtype=int)
        if len(Bvec) != n:
            raise Exception(f"Vector b must be length {n}")
        self.A = Amat
        self.b = Bvec
        self.n = n
        if alphabet in cipherAlphabets:
            self.alphabet = cipherAlphabets[alphabet]
        else:
            self.alphabet = alphabet
        self.k = len(self.alphabet)
        # Mod inverse of A mod k
        self.Ainv = self.ModMatInv(self.A,self.k)
        if self.Ainv is None:
            raise Exception(f"Matrix A is not invertible mod {self.k}")
    def ModMatInv(self,A,mod):
        n = A.shape[0]
        # Provides augmented matrix [A|I]
        aug = np.hstack((A.astype(int),np.identity(n,dtype=int)))
        for column in range(n):
            # Need to find pivot row
            pivot = None
            for row  in range(column,n):
                if aug[row,column]%mod != 0:
                    pivot = row
                    break
            if pivot is None:
                return None # Not invertible
                # Swapping pivot row with current row
            if pivot != column:
                aug[[column,pivot]]=aug[[pivot,column]]
            # Making pivot 1 by finding inverse
            pivotValue = aug[column,column]%mod
            invPivot = None
            for i in range(mod):
                if (pivotValue*i)%mod==1:
                    invPivot = i
                    break
            if invPivot is None:
                return None
            aug[column]=(aug[column]*invPivot)%mod
            # Elimination
            for row in range(n):
                if row!=column:
                    factor = aug[row,column]
                    if factor !=0:
                        aug[row]=(aug[row]-factor*aug[column])%mod
        return aug[:,n:].astype(int)
    def blockTransform(self,index,encode=True):
        # Allows us to transform block of indices length n
        x=np.array(index)
        if encode:
            y=(self.A@x+self.b)%self.k
        else:
            y=(self.Ainv@(x-self.b))%self.k
        return y.tolist()
    def process(self,text,encode=True):
        '''Transforms cipherAlphabets characters'''
        # Collecting positions and indices from alphabet characters
        pos = []
        indices = []
        for i,char in enumerate(text):
            lower=char.lower()
            if lower in self.alphabet:
                idx = self.alphabet.index(lower)
                pos.append(i)
                indices.append(idx)
        # Processing blocks
        newIndices = indices.copy()
        numBlocks = len(indices)//self.n
        for block in range(numBlocks):
            begin = block*self.n
            blk = indices[begin:begin+self.n]
            transformed = self.blockTransform(blk,encode)
            for j in range(self.n):
                newIndices[begin+j]=transformed[j]
        # Now we need to rebuild our string
        result = list(text)
        for position,newIndex in zip(pos,newIndices): # using zip() to convert the pos and newIndices lists into tuples
            original = text[position]
            newChar = self.alphabet[newIndex]
            result[position] = newChar.upper() if original.isupper() else newChar
        return ''.join(result)
    def encode(self,plaintext):
        return self.process(plaintext,encode=True)
    def decode(self,ciphertext):
        return self.process(ciphertext,encode=False)
    def demonstrate(self,messages):
        print("\n"+"="*80)
        print(f"Affine Hill Cipher (block size = {self.n}, alphabet = {self.alphabet})")
        print("="*80)
        for name, message in messages:
            encoded = self.encode(message)
            decoded = self.decode(encoded)
            print(f'\n{name} encoded and decoded:')
            print(f'Original: {message}')
            print(f'Encoded: {encoded}')
            print(f'Decoded: {decoded}')
    # Overloading for C2
    def __compose__(self,second):
        return CipherCompositionHill([second,self])
    def __pow__(self,exponent):
        if not isinstance(exponent,int) or exponent < 0:
            raise Exception('Exponent must be non-negative integer.')
        if exponent == 0:
            return IdentityHill(self.alphabet,self.n)
        ciphers = [self]*exponent
        return CipherCompositionHill(ciphers)
    def __mul__(self,scalar):
        if not isinstance(scalar,int):
            raise Exception('Scalar must be an integer')
        return AffineHillCipher(self.A,scalar*self.b,self.alphabet)
    def __rmul__(self,scalar):
        return self.__mul__(scalar)
    def __add__(self,second):
        if not np.array_equal(self.A,second.A):
            raise Exception('Addition only valid with identical A')
        if self.alphabet != second.alphabet:
            raise Exception('Addition requires identical alphabet')
        return AffineHillCipher(self.A,(self.b+second.b)%self.k,self.alphabet)
class IdentityHill(object):
    def __init__(self,alphabet,n):
        self.alphabet = alphabet
        self.n=n
    def encode(self,text):
        return text
    def decode(self,text):
        return text
    def __compose__(self,second):
        return second
    def __pow__(self,exponent):
        return self
    def demonstrate(self,messages):
        print("Identity cipher")
        return self
A = np.array([[2,1],[1,1]],dtype=int)
b = np.array([1,0],dtype=int)
cipher = AffineHillCipher(A,b)
cipher.demonstrate(messages)
# Justification
# I imported NumPy for linear algebra, allowing A and b to be stored as np arrays. I used matrix multiplication @ in my code for efficacy and conciseness, especially for larger block size n. Calculating A_inv requires Gaussian elimination over mod k, where k is the size of the alphabet chosen. This is much faster than finding the inverse for every block. I created a process function to process each block of size n, where incomplete blocks are not changed, since numBlocks uses integer division. It tracks the position of each original index of each alphabet character, allowing transformed characters to be placed in the same position. I used str.join for fast string construction as well. For decoding to be possible, A must be invertible mod k, meaning gcd(det(A),k)=1, and will raise an exception if not. My code creates A_inv, the inverse of A to check this (it cannot be created if A is not invertible). n can be any positive integer, and b can be an integer vector of length n. There are no restrictions on b. To construct an example, we choose an alphabet from cipherAlphabets (or your own), and pick a block size n. We need to then find an nxn integer matrix A, whose determinant is coprime with the size of the chosen alphabet. We now pick any integer vector b of length n, and can use AffineHillCipher(A,b,alphabet).

# Operations on Affine Hill Cipher
# 1 
A = np.array([[2,1],[1,1]],dtype=int)
b = np.array([1,0],dtype=int)
A2 = np.array([[2,0],[0,3]],dtype=int) # Invertible mod 5 (vowels size)
b2 = np.array([2,3],dtype=int)
comp1 = AffineHillCipher(A,b).__compose__(AffineHillCipher(A2,b2))
comp1.demonstrate(messages)
# 2 
exp2 = AffineHillCipher(A,b)**3
exp2.demonstrate(messages)
# 3
mult3 = (-1)*AffineHillCipher(A,b)
mult3.demonstrate(messages)
# 4
bPrime = np.array([2,1],dtype=int) # Distinct b
add4 = AffineHillCipher(A,b)+AffineHillCipher(A,bPrime)
add4.demonstrate(messages)
# Justification
# To support operators I used operator overloading such as: compose to return CipherCompostionHill, similar to the Caesar composition class, storing a list of ciphers, applying them sequentially. pow repeated the cipher exponent times, returning IdentityHill if exponent == 0 mul/rmul for scalar multiplication on b. Negation also works add adds two b vectors if A are identical, and alphabets match, otherwise exceptions are raised. Choosing A_2, it must be invertible mod k, where k is the size of the alphabet 'vowels', size 5. Since det(A_2)=6=1 (mod 5), it is invertible.
