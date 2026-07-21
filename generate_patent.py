import sys
import subprocess
import os

try:
    import docx
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-docx"])
    import docx

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level=level)
    h.paragraph_format.space_before = Pt(12)
    h.paragraph_format.space_after = Pt(6)
    return h

def add_paragraph(doc, text, indent=False):
    p = doc.add_paragraph(text)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    if indent:
        p.paragraph_format.first_line_indent = Inches(0.5)
    return p

def add_claim(doc, number, text):
    p = doc.add_paragraph(f"{number}. {text}")
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
    p.paragraph_format.left_indent = Inches(0.5)
    p.paragraph_format.first_line_indent = Inches(-0.5)
    return p

def create_patent_doc(filename):
    doc = Document()
    
    # Title
    title = doc.add_heading('SYSTEM, METHOD, AND COMPUTER-READABLE MEDIUM FOR LATENT SOURCE RECOVERY AND CONTINUOUS IDENTITY ATTRIBUTION IN MULTI-TARGET PHYSIOLOGICAL MONITORING', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Field of Invention
    add_heading(doc, 'FIELD OF THE INVENTION', level=1)
    add_paragraph(doc, 
        "[0001] The present invention relates generally to the field of non-invasive physiological monitoring. More specifically, "
        "the invention relates to signal processing architectures for multi-occupant environments, providing systems and methods "
        "for recovering, attributing, and maintaining the continuous identity of latent physiological signals extracted from "
        "mixed sensor arrays.", indent=True)

    # Background
    add_heading(doc, 'BACKGROUND OF THE INVENTION', level=1)
    add_paragraph(doc, 
        "[0002] Non-invasive physiological monitoring, particularly sleep monitoring using under-mattress sensors, has gained significant "
        "popularity. Such systems utilize force sensors, piezo-electric films, or strain gauges to detect ballistocardiographic "
        "(BCG) and respiratory efforts. However, when monitoring multiple subjects in close proximity (e.g., a double bed), "
        "the sensors inexorably capture a mixed signal containing overlapping physiological data and noise from both subjects.", indent=True)
    add_paragraph(doc,
        "[0003] Prior art systems attempt to resolve this cross-talk by relying on discrete movement events. For example, traditional "
        "methods determine which subject moved by comparing the signal amplitude of a sudden movement and measuring the time delay "
        "between the movement registering on a first sensor versus a second sensor. If the movement registers stronger and earlier "
        "on the left sensor, it is attributed to the left occupant. While functional for isolated movements, these methodologies "
        "fail dramatically during continuous periods of rest, simultaneous movement, or when occupants roll over into each other's "
        "respective sensor zones. Because traditional systems do not disentangle the continuous underlying physiological waveforms "
        "(i.e., the latent sources), they are highly susceptible to 'identity swapping'—where the system mistakenly assigns the "
        "heart rate of Subject A to Subject B following a complex physical shift.", indent=True)
    add_paragraph(doc,
        "[0004] Therefore, there exists a profound need in the art for a physiological monitoring system capable of blindly separating "
        "mixed physiological signals into continuous latent source streams, assigning those streams with probabilistic confidence, "
        "and persistently tracking identities to ensure high-fidelity longitudinal data.", indent=True)

    # Summary
    add_heading(doc, 'SUMMARY OF THE INVENTION', level=1)
    add_paragraph(doc, 
        "[0005] The present invention satisfies the aforementioned need by disclosing a robust, three-engine signal processing architecture "
        "capable of isolating and continuously tracking physiological signatures from multiple occupants in a shared environment.", indent=True)
    add_paragraph(doc,
        "[0006] In one aspect of the present invention, a Source Recovery Engine receives raw, mixed signal streams from a multi-channel "
        "sensor array. Rather than searching for discrete amplitude thresholds indicative of movement, the Source Recovery Engine "
        "applies a Blind Source Separation (BSS) algorithm, such as Independent Component Analysis (ICA), across sliding time windows "
        "to mathematically reconstruct the latent, independent physiological waveforms of each occupant.", indent=True)
    add_paragraph(doc,
        "[0007] In another aspect, an Occupant Attribution Engine analyzes the reconstructed latent waveforms. It cross-correlates the "
        "separated sources with the original mixed signals to determine a spatial footprint, fusing this with respiration "
        "synchronization and signal variance metrics. The engine outputs an identity assignment accompanied by a calculated "
        "Attribution Confidence Score.", indent=True)
    add_paragraph(doc,
        "[0008] In yet another aspect, an Identity Persistence Engine acts as a temporal state machine. It evaluates the current identity "
        "assignment against a historical identity mapping. The Identity Persistence Engine enforces a hysteresis constraint wherein "
        "a proposed identity swap (e.g., indicating the occupants have traded physical positions) is rejected unless the Attribution "
        "Confidence Score strictly exceeds a predefined high-confidence threshold. This effectively eliminates erroneous identity "
        "swapping caused by transient noise or simultaneous movement.", indent=True)

    # Brief Description of the Drawings
    add_heading(doc, 'BRIEF DESCRIPTION OF THE DRAWINGS', level=1)
    add_paragraph(doc, "[0009] FIG. 1 illustrates an overview of the multi-target physiological monitoring system 100.", indent=True)
    add_paragraph(doc, "[0010] FIG. 2 shows a block diagram of the three-engine signal processing architecture.", indent=True)
    add_paragraph(doc, "[0011] FIG. 3 illustrates the operations within the Data Acquisition Layer 110.", indent=True)
    add_paragraph(doc, "[0012] FIG. 4 is a flow diagram detailing the Source Recovery Engine 200 operations.", indent=True)
    add_paragraph(doc, "[0013] FIG. 5 illustrates the application of the Blind Source Separation algorithm 204.", indent=True)
    add_paragraph(doc, "[0014] FIG. 6 is a block diagram of the Occupant Attribution Engine 300 logic.", indent=True)
    add_paragraph(doc, "[0015] FIG. 7 illustrates the Identity Persistence Engine 400 state machine.", indent=True)
    add_paragraph(doc, "[0016] FIG. 8 is a flowchart of a method for continuous physiological monitoring.", indent=True)

    # Detailed Description
    add_heading(doc, 'DETAILED DESCRIPTION OF THE INVENTION', level=1)
    
    add_paragraph(doc,
        "[0017] The following detailed description illustrates embodiments of the present disclosure. These embodiments are described "
        "in sufficient detail to enable those skilled in the art to practice the invention, and it is to be understood that other "
        "embodiments may be utilized and that logical, architectural, and algorithmic changes may be made without departing from "
        "the spirit or scope of the present invention. Reference is made to FIGS. 1-8 which illustrate various aspects of the invention.", indent=True)

    add_heading(doc, 'The Data Acquisition Layer', level=2)
    add_paragraph(doc,
        "[0018] Referring to FIG. 3, the multi-target physiological monitoring system 100 comprises a Data Acquisition Layer 110 having a sensor array 102 configured for placement in proximity to the subjects. In a preferred embodiment, "
        "the sensor array 102 comprises at least two high-sensitivity strain gauges 104, piezoelectric strips, or hydraulic sensors "
        "disposed beneath a mattress. An analog-to-digital converter (ADC) 106 samples the signals at a high frequency (e.g., 100 Hz). "
        "The raw data is continuously buffered into overlapping or non-overlapping temporal windows (e.g., 10-second intervals) "
        "for batch processing within a buffer 112.", indent=True)

    add_heading(doc, 'The Source Recovery Engine', level=2)
    add_paragraph(doc,
        "[0019] As shown in FIGS. 4 and 5, the buffered mixed signals are passed to the Source Recovery Engine 200. First, a bandpass filter 202 isolates specific frequency "
        "bands of physiological interest, such as 0.8 Hz to 3.0 Hz for human heart rate. Following filtration, the Source Recovery Engine 200 executes "
        "a Blind Source Separation (BSS) algorithm 204. Unlike time-delay methodologies of the prior art, the BSS algorithm 204 mathematically decomposes "
        "the mixed multi-channel signal into a set of maximally independent latent source components. In a preferred embodiment, "
        "FastICA (Fast Independent Component Analysis) is utilized to generate a set of continuous, disentangled waveforms corresponding "
        "to the individual physiological rhythms (e.g., ballistocardiogram signatures) of each occupant.", indent=True)

    add_heading(doc, 'The Occupant Attribution Engine', level=2)
    add_paragraph(doc,
        "[0020] Referring to FIG. 6, because BSS algorithms inherently suffer from permutation ambiguity (the order of the output sources is random), the Occupant "
        "Attribution Engine 300 must resolve which latent source corresponds to which physical occupant. The Occupant Attribution Engine 300 calculates a spatial "
        "fingerprint 302 for each latent source by determining its cross-correlation with the raw, unfiltered signals originating from specific "
        "physical locations (e.g., Left Sensor vs. Right Sensor). By fusing spatial correlation, signal energy, and historical baseline "
        "metrics, the Occupant Attribution Engine 300 formulates a probabilistic assignment matrix 304. The difference between the highest and second-highest assignment "
        "probabilities is mapped to an Attribution Confidence Score 306.", indent=True)

    add_heading(doc, 'The Identity Persistence Engine', level=2)
    add_paragraph(doc,
        "[0021] As illustrated in FIG. 7 and FIG. 8, continuous physiological monitoring is highly susceptible to momentary artifacts. The Identity Persistence Engine 400 prevents "
        "transient assignment errors from corrupting longitudinal sleep metrics. The Identity Persistence Engine 400 maintains a running memory of the active "
        "identity mapping 402 via a state machine 404. If the Occupant Attribution Engine 300 proposes a mapping that contradicts the active identity mapping 402 (e.g., suggesting "
        "Subject A is now on the Right Sensor), the Identity Persistence Engine 400 evaluates the Attribution Confidence Score 306 against a "
        "pre-configured swap-threshold (e.g., 80% confidence). If the threshold is not met, the proposed swap is rejected as noise, "
        "and the active identity mapping 402 is persisted. If the threshold is exceeded, the swap is approved, accommodating legitimate physical "
        "crossover events without losing the continuous physiological thread of either subject.", indent=True)

    doc.add_page_break()

    # Claims
    add_heading(doc, 'CLAIMS', level=1)
    add_paragraph(doc, "What is claimed is:")
    
    claims = [
        "A method for continuous, multi-target physiological monitoring in a shared environment, the method comprising:\n"
        "receiving, from a sensor array, a plurality of mixed physiological signals spanning a temporal window;\n"
        "reconstructing, via a processor executing a Source Recovery Engine, a plurality of continuous latent physiological source streams from the mixed physiological signals, wherein the reconstruction is performed independently of discrete movement event detection;\n"
        "calculating, via an Occupant Attribution Engine, an attribution mapping and a corresponding confidence score for each reconstructed latent physiological source stream based on a correlation between the reconstructed stream and the plurality of mixed physiological signals; and\n"
        "maintaining, via an Identity Persistence Engine, a longitudinal identity association for each target by enforcing a state machine constraint, wherein an existing longitudinal identity association is overridden only if the calculated confidence score exceeds a predefined threshold.",
        
        "The method of claim 1, wherein reconstructing the plurality of continuous latent physiological source streams comprises applying a Blind Source Separation (BSS) algorithm to the mixed physiological signals.",
        
        "The method of claim 2, wherein the Blind Source Separation (BSS) algorithm is Independent Component Analysis (ICA).",
        
        "The method of claim 1, further comprising applying a bandpass filter to the mixed physiological signals prior to reconstructing the latent physiological source streams, wherein the bandpass filter isolates frequencies corresponding to human cardiac or respiratory activity.",
        
        "The method of claim 1, wherein calculating the attribution mapping comprises generating a spatial footprint by calculating a cross-correlation matrix between the continuous latent physiological source streams and the raw mixed physiological signals.",
        
        "The method of claim 1, wherein maintaining the longitudinal identity association comprises rejecting an attribution mapping that swaps target identities if the confidence score falls below 80 percent.",
        
        "The method of claim 1, wherein the sensor array comprises at least two unobtrusive sensors selected from the group consisting of strain gauges, piezoelectric elements, and hydraulic sensors.",
        
        "A multi-target physiological monitoring system, comprising:\n"
        "a sensor array configured to acquire a plurality of mixed physiological signals;\n"
        "a processor communicatively coupled to the sensor array;\n"
        "a non-transitory computer-readable medium storing instructions that, when executed by the processor, cause the system to:\n"
        "  buffer the acquired mixed physiological signals into a temporal window;\n"
        "  isolate a plurality of independent latent physiological waveforms from the temporal window using blind source separation;\n"
        "  generate a spatial footprint for each isolated latent physiological waveform to determine an identity assignment mapping and a confidence metric; and\n"
        "  persist a historical identity assignment mapping across sequential temporal windows, wherein the system rejects a change to the historical identity assignment mapping unless the confidence metric surpasses a defined swapping threshold.",
        
        "The system of claim 8, wherein isolating the plurality of independent latent physiological waveforms is performed exclusively on continuous resting physiological data without requiring the detection of a movement event amplitude or time delay.",
        
        "The system of claim 8, wherein the sensor array is adapted to be positioned beneath a mattress, and the independent latent physiological waveforms correspond to individual ballistocardiogram signatures of occupants sharing the mattress."
    ]

    for i, claim_text in enumerate(claims, 1):
        add_claim(doc, i, claim_text)

    doc.add_page_break()
    
    # Abstract
    add_heading(doc, 'ABSTRACT OF THE DISCLOSURE', level=1).alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_paragraph(doc, 
        "[0000] A system and method for continuous, multi-target physiological monitoring that separates and persistently tracks "
        "signals from multiple subjects sharing a monitored environment. The system comprises a sensor array to capture a "
        "plurality of mixed physiological signals. A Source Recovery Engine actively reconstructs continuous latent physiological "
        "streams from the mixed signals using blind source separation techniques, bypassing reliance on discrete movement events. "
        "An Occupant Attribution Engine assigns the recovered streams to respective subjects based on a multi-dimensional spatial "
        "and temporal confidence score. An Identity Persistence Engine maintains longitudinal identity associations using a state "
        "machine that overrides existing identity mappings only if an attribution confidence metric surpasses a predefined high-confidence "
        "threshold. The invention prevents identity swapping during simultaneous movement or sensor zone crossover.", 
        indent=True)

    # Drawings Section
    image_files = [
        'Technical diagram of heart signal processing.png',
        'Technical diagram of heart signal processing2.png',
        'Technical diagram of heart signal processing3.png',
        'Technical diagram of heart signal processing4.png',
        'Technical diagram of heart signal processing5.png',
        'Technical diagram of heart signal processing6.png',
        'Technical diagram of heart signal processing7.png',
        'Technical diagram of heart signal processing8.png'
    ]
    
    for i, img_file in enumerate(image_files, 1):
        if i % 2 != 0:
            doc.add_page_break()
        if os.path.exists(img_file):
            doc.add_picture(img_file, height=Inches(3.5))
            p = doc.add_paragraph(f'FIG. {i}')
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_before = Pt(6)
            if i % 2 != 0:
                p.paragraph_format.space_after = Pt(24)
        else:
            print(f"Warning: Could not find {img_file}")

    doc.save(filename)
    print(f"Successfully generated better patent doc at {filename}")

if __name__ == '__main__':
    create_patent_doc(r"d:\SleepAnalyzer\Professional_Patent_Draft_v2.docx")
