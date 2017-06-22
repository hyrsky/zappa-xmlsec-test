import xmlsec
from flask import Flask

from os import path
from lxml import etree

app = Flask(__name__)

BASE_DIR = path.dirname(__file__)

def parse_xml(name):
    return etree.parse(path.join(BASE_DIR, name)).getroot()

def compare(name, result):
    # Parse the expected file.
    xml = parse_xml(name)

    # Stringify the root, <Envelope/> nodes of the two documents.
    expected_text = etree.tostring(xml, pretty_print=False)
    result_text = etree.tostring(result, pretty_print=False)

    # Compare the results.
    assert expected_text == result_text


def test_sign_generated_template_pem_with_x509():
    """
    Should sign a file using a dynamicaly created template, key from PEM
    file and an X509 certificate.
    """

    # Load document file.
    template = parse_xml('sign3-doc.xml')

    # Create a signature template for RSA-SHA1 enveloped signature.
    signature_node = xmlsec.template.create(
	    template,
	    xmlsec.Transform.EXCL_C14N,
	    xmlsec.Transform.RSA_SHA1)

    assert signature_node is not None

    # Add the <ds:Signature/> node to the document.
    template.append(signature_node)

    # Add the <ds:Reference/> node to the signature template.
    ref = xmlsec.template.add_reference(signature_node, xmlsec.Transform.SHA1)

    # Add the enveloped transform descriptor.
    xmlsec.template.add_transform(ref, xmlsec.Transform.ENVELOPED)

    # Add the <ds:KeyInfo/> and <ds:KeyName/> nodes.
    key_info = xmlsec.template.ensure_key_info(signature_node)
    xmlsec.template.add_x509_data(key_info)

    # Create a digital signature context (no key manager is needed).
    ctx = xmlsec.SignatureContext()

    # Load private key (assuming that there is no password).
    filename = path.join(BASE_DIR, 'rsakey.pem')
    key = xmlsec.Key.from_file(filename, xmlsec.KeyFormat.PEM)

    assert key is not None

    # Load the certificate and add it to the key.
    filename = path.join(BASE_DIR, 'rsacert.pem')
    key.load_cert_from_file(filename, xmlsec.KeyFormat.PEM)

    # Set key name to the file name (note: this is just a test).
    key.name = path.basename(filename)

    # Set the key on the context.
    ctx.key = key

    assert ctx.key is not None
    assert ctx.key.name == path.basename(filename)

    # Sign the template.
    ctx.sign(signature_node)

    # Assert the contents of the XML document against the expected result.
    compare('sign3-res.xml', template)

@app.route('/')
def hello_world():
    test_sign_generated_template_pem_with_x509

    return 'Hello, world!'

if __name__ == '__main__':
    app.run()
